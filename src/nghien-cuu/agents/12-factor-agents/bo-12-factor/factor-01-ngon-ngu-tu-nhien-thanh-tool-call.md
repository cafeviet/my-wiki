# Factor 1: Natural Language to Tool Calls (Chuyển đổi Ngôn ngữ Tự nhiên thành Lệnh gọi Công cụ)

> **Nguồn gốc:** [humanlayer/12-factor-agents — `content/factor-01-natural-language-to-tool-calls.md`](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-01-natural-language-to-tool-calls.md) (commit `d20c728`)
> 
> **Bộ bài:** [12-Factor Agents — bản dịch toàn văn](./)

`[Dịch]` Một trong những thiết kế mẫu (design pattern) cốt lõi và phổ biến nhất khi xây dựng hệ thống Agent là **chuyển đổi ngôn ngữ tự nhiên thành các lệnh gọi công cụ có cấu trúc định kiểu (Typed Tool Calls)**. Đây là cơ chế nền tảng cho phép kết nối khả năng suy luận xác suất của LLM với các hệ thống phần mềm tất định (Deterministic Execution).

![Ngôn ngữ tự nhiên → lệnh gọi tool có cấu trúc](/nghien-cuu/agents/12-factor-agents/assets/img/110-natural-language-tool-calls.png)

`[Dịch]` Khi áp dụng ở mức độ nguyên tử (atomic operation), mẫu thiết kế này đơn giản là việc biên dịch một yêu cầu phi cấu trúc như:

> "Bạn có thể tạo một payment link $750 cho Terri vì đã tài trợ buổi meetup AI Tinkerers tháng Hai không?"

thành một đối tượng JSON có cấu trúc định kiểu rõ ràng, mô tả đầy đủ tham số cho lệnh gọi Stripe API:

```json
{
  "function": {
    "name": "create_payment_link",
    "parameters": {
      "amount": 750,
      "customer": "cust_128934ddasf9",
      "product": "prod_8675309",
      "price": "prc_09874329fds",
      "quantity": 1,
      "memo": "Hey Jeff - see below for the payment link for the february ai tinkerers meetup"
    }
  }
}
```

`[Dịch]` **Lưu ý kiến trúc:** Trên thực tế, quy trình tích hợp API của Stripe phức tạp hơn; một [Agent thực tế triển khai bài toán này](https://github.com/dexhorthy/mailcrew) ([video demo](https://www.youtube.com/watch?v=f_cKnoPC_Oo)) sẽ cần truy vấn danh sách khách hàng, danh mục sản phẩm, bảng giá tương ứng để thu thập các định danh (ID) chính xác nhằm dựng payload này, hoặc nạp trước các ID đó vào context window (chúng ta sẽ thấy ở các Factor sau rằng hai cách tiếp cận này có sự tương đồng sâu sắc).

`[Dịch]` Từ payload có cấu trúc này, tầng mã nguồn tất định (Deterministic Code) sẽ tiếp nhận, xác thực (validate) và điều phối thực thi:

```python
# LLM tiếp nhận prompt ngôn ngữ tự nhiên và phân giải thành Action Schema có cấu trúc
nextStep = await llm.determineNextStep(
    """
    create a payment link for $750 to Jeff
    for sponsoring the february AI tinkerers meetup
    """
)

# Dispatching thực thi tất định dựa trên Function Identifier
if nextStep.function == 'create_payment_link':
    stripe.paymentlinks.create(**nextStep.parameters)
    return  # Hoặc xử lý tiếp theo luồng nghiệp vụ
elif nextStep.function == 'something_else':
    # Xử lý các nhánh nghiệp vụ khác
    pass
else:
    # Fallback khi mô hình sinh lệnh gọi không khớp schema hợp lệ
    pass
```

`[Dịch]` **Lưu ý kiến trúc (Architectural Note):** Một Agent hoàn chỉnh thông thường sẽ nhận kết quả phản hồi từ API, đưa vào vòng lặp suy luận tiếp theo và trả về phản hồi cuối cùng cho người dùng dạng:

> "Tôi đã tạo thành công link thanh toán $750 cho Terri cho sự kiện tài trợ AI Tinkerers tháng Hai. Link thanh toán: https://buy.stripe.com/test_1234567890"

`[Dịch]` **Tuy nhiên**, ở Factor 1, chúng ta chủ ý cô lập thao tác này ở mức nguyên tử (Atomic Tool Call) mà chưa vội ghép nối vòng lặp tự trị phức tạp — việc điều phối vòng lặp và quản lý trạng thái sẽ được phân rã thành các nguyên lý kiến trúc độc lập tiếp theo.

---

**Điều hướng:** [← Vì sao lại là 12-factor agents?](./vi-sao-12-factor.md) · [Mục lục](./) · [Factor 2: Own your prompts →](./factor-02-so-huu-prompt.md)

