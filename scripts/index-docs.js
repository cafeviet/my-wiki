import fs from 'fs';
import path from 'path';
import * as lancedb from '@lancedb/lancedb';
import { pipeline } from '@huggingface/transformers';

const SRC_DIR = path.join(process.cwd(), 'src');
const DB_DIR = path.join(process.cwd(), 'data/wiki-vector-db');

// Danh sách các folder tài liệu muốn quét
const WATCHED_DIRS = ['tai-lieu', 'nghien-cuu', 'dich-thuat'];

// 1. Khởi tạo mô hình AI sinh Vector (Embedding Model)
console.log("Đang tải mô hình sinh Vector Embedding (Xenova/all-MiniLM-L6-v2)...");
const extractor = await pipeline('feature-extraction', 'Xenova/all-MiniLM-L6-v2');

async function getEmbedding(text) {
  const output = await extractor(text, { pooling: 'mean', normalize: true });
  return Array.from(output.data);
}

// 2. Chunker: Hàm chia nhỏ văn bản theo đoạn văn có logic
function chunkText(text, maxChunkSize = 800, overlap = 150) {
  const paragraphs = text.split(/\n\s*\n/);
  const chunks = [];
  let currentChunk = '';

  for (const para of paragraphs) {
    const p = para.trim();
    if (!p) continue;

    if ((currentChunk + '\n\n' + p).length <= maxChunkSize) {
      if (currentChunk) currentChunk += '\n\n' + p;
      else currentChunk = p;
    } else {
      if (currentChunk) chunks.push(currentChunk);

      if (p.length > maxChunkSize) {
        // Cắt theo độ dài ký tự nếu có đoạn văn quá dài
        let start = 0;
        while (start < p.length) {
          const end = Math.min(start + maxChunkSize, p.length);
          chunks.push(p.slice(start, end));
          start += maxChunkSize - overlap;
        }
        currentChunk = '';
      } else {
        currentChunk = p;
      }
    }
  }
  if (currentChunk) {
    chunks.push(currentChunk);
  }
  return chunks;
}

// 3. Hàm đệ quy quét tất cả file .md
function getMdFiles(dir) {
  let results = [];
  const list = fs.readdirSync(dir);
  
  list.forEach((file) => {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);
    
    if (stat && stat.isDirectory()) {
      if (file !== '.vitepress' && file !== 'node_modules') {
        results = results.concat(getMdFiles(filePath));
      }
    } else if (file.endsWith('.md')) {
      results.push(filePath);
    }
  });
  
  return results;
}

// 4. Xử lý chính
async function main() {
  console.log("Bắt đầu quét tài liệu...");
  
  // Lấy tất cả file .md trong các folder chỉ định
  let allFiles = [];
  WATCHED_DIRS.forEach((dirName) => {
    const targetPath = path.join(SRC_DIR, dirName);
    if (fs.existsSync(targetPath)) {
      allFiles = allFiles.concat(getMdFiles(targetPath));
    }
  });

  if (allFiles.length === 0) {
    console.log("Không tìm thấy file Markdown nào trong các thư mục tài liệu mẫu.");
    return;
  }

  console.log(`Tìm thấy ${allFiles.length} file tài liệu cần xử lý.`);
  const dataset = [];

  for (const filePath of allFiles) {
    const content = fs.readFileSync(filePath, 'utf-8');
    
    // Tách frontmatter bằng regex
    const frontmatterRegex = /^---\r?\n([\s\S]*?)\r?\n---\r?\n/;
    let body = content;
    let frontmatter = {};
    
    if (frontmatterRegex.test(content)) {
      const match = content.match(frontmatterRegex);
      body = content.replace(frontmatterRegex, '');
      
      // Parse frontmatter đơn giản
      match[1].split('\n').forEach(line => {
        const parts = line.split(':');
        if (parts.length >= 2) {
          const key = parts[0].trim();
          const value = parts.slice(1).join(':').trim();
          frontmatter[key] = value;
        }
      });
    }

    // Tìm tiêu đề
    let title = frontmatter.title;
    if (!title) {
      const titleMatch = body.match(/^#\s+(.+)$/m);
      title = titleMatch ? titleMatch[1].trim() : path.basename(filePath, '.md');
    }

    // Tính đường dẫn link trong trang web (VitePress route)
    let routePath = '/' + path.relative(SRC_DIR, filePath).replace(/\\/g, '/');
    if (routePath.endsWith('.md')) {
      routePath = routePath.slice(0, -3);
    }
    if (routePath.endsWith('/index')) {
      routePath = routePath.slice(0, -5);
    }
    if (routePath === '') routePath = '/';

    console.log(`Đang chia nhỏ và sinh Vector cho bài viết: "${title}" (${routePath})`);
    
    const chunks = chunkText(body);
    for (let i = 0; i < chunks.length; i++) {
      const chunkText = chunks[i];
      if (chunkText.trim().length < 10) continue; // Bỏ qua chunk quá ngắn

      const vector = await getEmbedding(chunkText);
      dataset.push({
        vector,
        text: chunkText,
        title: `${title} (Đoạn ${i + 1})`,
        link: routePath
      });
    }
  }

  console.log(`Chuẩn bị lưu ${dataset.length} vector vào LanceDB...`);
  
  // Đảm bảo thư mục lưu DB tồn tại
  const dataDir = path.dirname(DB_DIR);
  if (!fs.existsSync(dataDir)) {
    fs.mkdirSync(dataDir, { recursive: true });
  }

  const db = await lancedb.connect(DB_DIR);
  const table = await db.createTable("wiki_chunks", dataset, { mode: "overwrite" });
  
  console.log("Lập chỉ mục tài liệu thành công!");
  console.log(`Cơ sở dữ liệu Vector đã được lưu tại: ${DB_DIR}`);
}

main().catch(err => {
  console.error("Lỗi trong quá trình lập chỉ mục:", err);
});
