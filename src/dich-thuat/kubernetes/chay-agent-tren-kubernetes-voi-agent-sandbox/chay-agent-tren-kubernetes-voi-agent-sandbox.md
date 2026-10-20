# Chạy Agent trên Kubernetes với Agent Sandbox

> **Bản dịch tiếng Việt từ:** [Running Agents on Kubernetes with Agent Sandbox](https://kubernetes.io/blog/2026/03/20/running-agents-on-kubernetes-with-agent-sandbox/), Kubernetes Blog.
> **Tác giả:** Janet Kuo, Justin Santa Barbara.
> **Ngày xuất bản:** 20/03/2026.
> **Quy ước thuật ngữ:** Từ khóa quan trọng trình bày dạng **tiếng Việt (English)** ở lần đầu; tên sản phẩm, tên API/CRD và lệnh được giữ nguyên.

Bối cảnh **trí tuệ nhân tạo (artificial intelligence)** đang trải qua một bước dịch chuyển kiến trúc lớn. Ở thời kỳ đầu của **AI tạo sinh (generative AI)**, việc tương tác với một model thường được xem như một lời gọi hàm thoáng qua và phi trạng thái (stateless): một yêu cầu được khởi tạo, chạy trong khoảng 50 mili-giây rồi kết thúc.

Ngày nay, thế giới đang chứng kiến "AI v2 nuốt chửng AI v1". Hệ sinh thái đang chuyển từ những tác vụ ngắn hạn, đơn lẻ sang việc triển khai nhiều **agent** AI phối hợp với nhau và chạy liên tục. Những agent tự chủ này cần duy trì ngữ cảnh, sử dụng công cụ (tools) bên ngoài, viết và thực thi mã, đồng thời giao tiếp với nhau trong những khoảng thời gian dài.

Khi các đội **kỹ thuật nền tảng (platform engineering)** tìm kiếm hạ tầng phù hợp để lưu trú các workload AI kiểu mới này, có một nền tảng nổi lên như lựa chọn tự nhiên: Kubernetes. Tuy nhiên, việc ánh xạ các workload agentic đặc thù này sang các **nguyên hàm (primitives)** truyền thống của Kubernetes lại đòi hỏi một tầng trừu tượng mới.

Đó chính là lúc dự án [Agent Sandbox](https://github.com/kubernetes-sigs/agent-sandbox) mới (hiện đang được phát triển trong SIG Apps) phát huy vai trò.

## Lợi thế của Kubernetes (và khoảng trống trừu tượng)

Kubernetes là chuẩn mực trên thực tế (de facto) để điều phối các ứng dụng **cloud-native**, chính vì nó giải quyết được các bài toán về khả năng mở rộng, mạng lưới vững chắc và độ trưởng thành của hệ sinh thái. Tuy nhiên, khi AI tiến hóa từ những yêu cầu **suy luận (inference)** ngắn hạn sang những agent tự chủ chạy dài hạn, chúng ta đang thấy xuất hiện một mô hình vận hành mới.

Ngược lại, các agent AI thường là những workload **đơn thể (singleton)**, có trạng thái (stateful) và bị cô lập. Chúng đóng vai trò như một không gian làm việc số hoặc môi trường thực thi cho một **LLM**. Một agent cần một danh tính bền vững (persistent identity) và một vùng nháp an toàn (secure scratchpad) để viết và thực thi mã — thường là mã không đáng tin cậy (untrusted). Điều quan trọng là vì các agent chạy dài này được kỳ vọng phần lớn thời gian ở trạng thái nhàn rỗi, chỉ hoạt động trong những đợt bùng ngắn, nên chúng cần một vòng đời (lifecycle) hỗ trợ các cơ chế như tạm ngưng (suspension) và khôi phục nhanh (rapid resumption).

Trong khi bạn có thể ghép lại với nhau một `StatefulSet` kích thước 1, một **Service** headless và một `PersistentVolumeClaim` cho từng agent, việc quản lý ở quy mô lớn theo cách này trở thành một cơn ác mộng vận hành.

Vì những đặc tính đặc thù này, các nguyên hàm truyền thống của Kubernetes không khớp hoàn hảo.

## Giới thiệu Kubernetes Agent Sandbox

Để lấp khoảng trống này, SIG Apps đang phát triển [agent-sandbox](https://github.com/kubernetes-sigs/agent-sandbox). Dự án giới thiệu một **API khai báo (declarative), chuẩn hóa** được thiết kế riêng cho các workload đơn thể, có trạng thái như các **runtime** agent AI.

Ở lõi, dự án giới thiệu **Sandbox CRD** (Custom Resource Definition). Nó hoạt động như một môi trường nhẹ, một-container, được xây dựng hoàn toàn trên các nguyên hàm Kubernetes, cung cấp:

- **Cô lập mạnh cho mã không đáng tin cậy (strong isolation for untrusted code):** Khi một agent AI tự sinh và thực thi mã một cách tự chủ, bảo mật là tối quan trọng. Custom resource Sandbox hỗ trợ sẵn nhiều runtime khác nhau như gVisor hoặc Kata Containers. Điều này cung cấp mức cô lập kernel và mạng cần thiết cho việc thực thi đa người thuê (multi-tenant), không đáng tin cậy.
- **Quản lý vòng đời (lifecycle management):** Khác với các web server truyền thống được tối ưu cho lưu lượng ổn định, phi trạng thái, một agent AI vận hành như một không gian làm việc có trạng thái, có thể nhàn rỗi hàng giờ giữa các tác vụ. Agent Sandbox hỗ trợ **thu giảm các môi trường nhàn rỗi về mức 0 (scale to zero)** để tiết kiệm tài nguyên, đồng thời đảm bảo chúng có thể tiếp tục đúng từ điểm đã dừng.
- **Danh tính ổn định (stable identity):** Các hệ thống đa agent phối hợp đòi hỏi mạng lưới ổn định. Mỗi Sandbox được cấp một hostname và danh tính mạng ổn định, cho phép các agent riêng biệt khám phá và giao tiếp với nhau một cách liền mạch.

## Mở rộng quy mô agent bằng các Extension

Vì lĩnh vực AI đang chuyển động cực kỳ nhanh, chúng tôi đã xây dựng một tầng **Extensions API** cho phép lặp và phát triển nhanh hơn nữa.

Khởi động một pod mới tốn thêm khoảng một giây chi phí (overhead). Điều đó hoàn toàn ổn khi triển khai một phiên bản mới của một microservice, nhưng khi một agent được gọi sau khi đã nhàn rỗi, một lần **khởi động nguội (cold start)** mất một giây sẽ phá vỡ tính liên tục của tương tác. Nó buộc người dùng hoặc dịch vụ điều phối phải chờ môi trường được cấp phát trước khi model kịp bắt đầu "suy nghĩ" hay hành động. **SandboxWarmPool** giải quyết vấn đề này bằng cách duy trì một pool các pod Sandbox đã cấp phát sẵn, qua đó loại bỏ hiệu quả các lần khởi động nguội. Người dùng hoặc dịch vụ điều phối chỉ cần phát ra một **SandboxClaim** đối với một **SandboxTemplate**, và controller lập tức bàn giao một môi trường đã được làm nóng sẵn, được cô lập hoàn toàn cho agent.

## Bắt đầu nhanh

Sẵn sàng tự trải nghiệm? Bạn có thể cài đặt các thành phần lõi và các extension của Agent Sandbox trực tiếp vào cluster học tập hoặc sandbox của bạn, dùng bản phát hành (release) bạn chọn.

Chúng tôi khuyến nghị dùng bản phát hành mới nhất vì dự án đang tiến triển rất nhanh.

```
# Thay "vX.Y.Z" bằng một tag phiên bản cụ thể (ví dụ "v0.1.0") từ
# https://github.com/kubernetes-sigs/agent-sandbox/releases
export VERSION="vX.Y.Z"

# Cài đặt các thành phần lõi:
kubectl apply -f https://github.com/kubernetes-sigs/agent-sandbox/releases/download/${VERSION}/manifest.yaml

# Cài đặt các thành phần extension (tùy chọn):
kubectl apply -f https://github.com/kubernetes-sigs/agent-sandbox/releases/download/${VERSION}/extensions.yaml

# Cài đặt Python SDK (tùy chọn):
# Tạo một môi trường Python ảo
python3 -m venv .venv
source .venv/bin/activate
# Cài đặt từ PyPI
pip install k8s-agent-sandbox
```

Sau khi cài đặt, bạn có thể thử [Python SDK](https://github.com/kubernetes-sigs/agent-sandbox/tree/main/clients/python/agentic-sandbox-client) dành cho agent AI, hoặc triển khai một trong các [ví dụ](https://github.com/kubernetes-sigs/agent-sandbox/tree/main/examples) dùng-ngay để thấy việc dựng một môi trường agent cô lập dễ dàng đến mức nào.

## Tương lai của agent là cloud native

Dù là một tác vụ phi trạng thái 50 mili-giây, hay một tiến trình cộng tác kéo dài nhiều tuần và phần lớn thời gian nhàn rỗi, việc mở rộng Kubernetes bằng các nguyên hàm được thiết kế riêng cho các **đơn thể có trạng thái, được cô lập (isolated stateful singletons)** cho phép chúng ta tận dụng toàn bộ lợi ích vững chắc của hệ sinh thái cloud-native.

Dự án Agent Sandbox là mã nguồn mở và do cộng đồng dẫn dắt. Nếu bạn đang xây dựng nền tảng AI, phát triển các framework agentic, hoặc quan tâm đến khả năng mở rộng của Kubernetes, chúng tôi mời bạn tham gia:

- Xem dự án trên GitHub: [kubernetes-sigs/agent-sandbox](https://github.com/kubernetes-sigs/agent-sandbox)
- Tham gia thảo luận tại các kênh [#sig-apps](https://kubernetes.slack.com/messages/sig-apps) và [#agent-sandbox](https://kubernetes.slack.com/messages/agent-sandbox) trên Kubernetes Slack.
