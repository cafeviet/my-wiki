import { defineConfig } from 'vitepress'
import { withSidebar } from 'vitepress-sidebar'
import * as lancedb from '@lancedb/lancedb'
import { pipeline } from '@huggingface/transformers'
import path from 'path'
import url from 'url'

// Biến toàn cục để cache mô hình AI và kết nối Database
let extractorPromise = null
let dbPromise = null

// Vite Plugin tạo API Endpoint cục bộ để tìm kiếm Vector
const localSearchApiPlugin = () => ({
  name: 'local-search-api',
  configureServer(server) {
    server.middlewares.use(async (req, res, next) => {
      const parsedUrl = url.parse(req.url, true)
      
      if (parsedUrl.pathname === '/api/search') {
        const queryText = parsedUrl.query.q
        
        if (!queryText) {
          res.writeHead(400, { 'Content-Type': 'application/json' })
          res.end(JSON.stringify({ error: 'Query parameter q is required' }))
          return
        }

        try {
          // 1. Tải model AI sinh vector (chỉ tải 1 lần và cache lại)
          if (!extractorPromise) {
            extractorPromise = pipeline('feature-extraction', 'Xenova/all-MiniLM-L6-v2')
          }
          const extractor = await extractorPromise

          // 2. Kết nối tới DB Vector LanceDB
          if (!dbPromise) {
            const dbPath = path.join(process.cwd(), 'data/wiki-vector-db')
            dbPromise = lancedb.connect(dbPath)
          }
          const db = await dbPromise

          // 3. Tính toán Vector cho từ khóa truy vấn
          const output = await extractor(queryText, { pooling: 'mean', normalize: true })
          const queryVector = Array.from(output.data)

          // 4. Tìm kiếm trong bảng LanceDB
          const table = await db.openTable("wiki_chunks")
          const results = await table.search(queryVector).limit(4).toArray()

          // 5. Trả về kết quả loại bỏ trường vector gốc để tối ưu tốc độ tải
          const cleanResults = results.map(item => ({
            text: item.text,
            title: item.title,
            link: item.link,
            _distance: item._distance
          }))

          res.writeHead(200, { 'Content-Type': 'application/json' })
          res.end(JSON.stringify(cleanResults))
        } catch (err) {
          console.error("Lỗi API Search:", err)
          res.writeHead(500, { 'Content-Type': 'application/json' })
          res.end(JSON.stringify({ error: err.message }))
        }
        return
      }
      next()
    })
  }
})

const vitePressConfig = {
  title: "Kho Tài Liệu Cá Nhân",
  description: "Hệ thống lưu trữ bài viết dịch thuật, nghiên cứu và tài liệu cá nhân cục bộ.",
  lang: 'vi-VN',
  srcDir: '.',
  cleanUrls: true,
  themeConfig: {
    logo: {
      light: 'https://img.icons8.com/fluency/48/library.png',
      dark: 'https://img.icons8.com/fluency/48/library.png',
      alt: 'Logo'
    },
    nav: [
      { text: 'Trang chủ', link: '/' },
      { text: 'Tài liệu', link: '/tai-lieu/' },
      { text: 'Nghiên cứu', link: '/nghien-cuu/' },
      { text: 'Dịch thuật', link: '/dich-thuat/' },
      { text: 'Trợ lý AI 🤖', link: '/chat' }
    ],
    search: {
      provider: 'local',
      options: {
        translations: {
          button: {
            buttonText: 'Tìm kiếm tài liệu...',
            buttonAriaLabel: 'Tìm kiếm tài liệu...'
          },
          modal: {
            noResultsText: 'Không tìm thấy tài liệu nào',
            resetButtonTitle: 'Xóa kết quả tìm kiếm',
            footer: {
              selectText: 'để chọn',
              navigateText: 'để di chuyển',
              closeText: 'để đóng'
            }
          }
        }
      }
    },
    outline: {
      label: 'Mục lục trang này',
      level: [2, 4]
    },
    docFooter: {
      prev: 'Trang trước',
      next: 'Trang sau'
    },
    lastUpdated: {
      text: 'Cập nhật gần nhất',
      formatOptions: {
        dateStyle: 'short',
        timeStyle: 'medium'
      }
    },
    darkModeSwitchLabel: 'Giao diện',
    lightModeSwitchTitle: 'Chuyển sang giao diện sáng',
    darkModeSwitchTitle: 'Chuyển sang giao diện tối',
    sidebarMenuLabel: 'Danh mục',
    returnToTopLabel: 'Trở lại đầu trang'
  },
  vite: {
    plugins: [localSearchApiPlugin()]
  }
}

export default defineConfig(
  withSidebar(vitePressConfig, [
    {
      documentRootPath: 'src',
      scanStartPath: 'tai-lieu',
      resolvePath: '/tai-lieu/',
      useTitleFromFileHeading: true,
      useFolderTitleFromIndexFile: true,
      useFolderLinkFromIndexFile: true,
      hyphenToSpace: true,
      keepMarkdownSyntaxFromTitle: true,
      collapsed: false,
      collapseDepth: 2
    },
    {
      documentRootPath: 'src',
      scanStartPath: 'nghien-cuu',
      resolvePath: '/nghien-cuu/',
      useTitleFromFileHeading: true,
      useFolderTitleFromIndexFile: true,
      useFolderLinkFromIndexFile: true,
      hyphenToSpace: true,
      keepMarkdownSyntaxFromTitle: true,
      collapsed: false,
      collapseDepth: 2
    },
    {
      documentRootPath: 'src',
      scanStartPath: 'dich-thuat',
      resolvePath: '/dich-thuat/',
      useTitleFromFileHeading: true,
      useFolderTitleFromIndexFile: true,
      useFolderLinkFromIndexFile: true,
      hyphenToSpace: true,
      keepMarkdownSyntaxFromTitle: true,
      collapsed: false,
      collapseDepth: 2
    }
  ])
)


