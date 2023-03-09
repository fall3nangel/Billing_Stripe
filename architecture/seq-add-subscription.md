```mermaid
---
title: Purchasing subscription (POST /add-subscription)
---
sequenceDiagram
    autonumber
    actor USER
    participant UserAPI
    participant BillingAPI
    participant PayAPI
    participant QUEUE
    USER->>+UserAPI: get invoice
    UserAPI->>+BillingAPI: get product(subscription) details
    BillingAPI->>BillingAPI: calc cost including discounts and promo
    BillingAPI->>BillingAPI: create invoice
    BillingAPI-->>-UserAPI: invoice
    UserAPI-->>-USER: invoice
    USER->>+UserAPI: make payment
    UserAPI->>+PayAPI: create payment
    PayAPI-->>-UserAPI: payment status
    UserAPI->>+BillingAPI: set payment
    BillingAPI->>BillingAPI: check status
    BillingAPI-->>-UserAPI: status
    UserAPI->>QUEUE: send notification
    UserAPI->>UserAPI: create/update role
    UserAPI->>UserAPI: refresh token
    UserAPI-->>-USER: token
```