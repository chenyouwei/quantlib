

### Example Usage

```python
def func():
    ind = get_mean_price_over_last_5_days()
    price = get_price(stock, 'close')

    if ((ind > 0.5) and (price < 10)__frequency):
        order_target_value(stock, price, amount)
```


trigger_price = 100
current_box = [105, 110]
current_day_highest_price = 100

# 多开

if trigger_price <= current_box.high:
   # 触发价格小于等于笼子的最高价格就触发
   # 成交价格设置为当日的涨停价格，一定成交
   knock_down_price = current_day_highest_price
   