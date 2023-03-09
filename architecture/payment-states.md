```mermaid
stateDiagram-v2
    [*] --> Created
    state authorize <<choice>>
    Created --> authorize
    authorize --> Authorized : корректные данные
    authorize --> NotApproved : некорректные ревизиты,\nотрицательный баланс
    Created --> Failed : сетевая ошибка
    Authorized --> Captured : списание со счета\nклиента подтверждено
    Authorized --> NotCaptured : списание со счета\nклиента не подтверждено
    NotCaptured --> Refunded : должен быть возвращен\nв течении суток
    Captured --> Refunded : может быть\nвозвращен клиентом

    NotApproved --> [*]
    Captured --> [*] : пополнение счета предприятия
    Failed --> [*]
    Refunded --> [*] : возврат клиенту

```
# Payment status

Status | Description         
---- |---------------------
created | Платеж передан в платежную систему, но еще не обработан.  
authorized | Реквизиты проверены, денежные средства списаны со счета клиента. Платеж возвращается клиенту, если он не будет зафиксирован.
captured | Денежные средства могут быть переданы на счет предприятия.
refunded | Платеж возвращен на счет клиента. 
failed | Неудачная попытка оплаты. 

