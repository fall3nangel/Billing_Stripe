```mermaid
---
title: Cancel payment (POST /cancel-payment)
---
sequenceDiagram
    autonumber
    actor USER
    participant UserAPI
    participant BillingAPI
    participant PayAPI
    participant QUEUE
    USER->>+UserAPI: get payment
    UserAPI->>+BillingAPI: get payment details
    BillingAPI-->>-UserAPI: payment
    UserAPI-->>-USER: payment
    USER->>+UserAPI: cancel payment
    UserAPI->>+PayAPI: cancel payment
    PayAPI-->>-UserAPI: payment status
    UserAPI->>+BillingAPI: delete payment
    BillingAPI->>BillingAPI: delete payment
    BillingAPI->>BillingAPI: check status
    BillingAPI-->>-UserAPI: status
    UserAPI->>QUEUE: send notification
    UserAPI->>UserAPI: update role
    UserAPI->>UserAPI: refresh token
    UserAPI-->>-USER: token
```