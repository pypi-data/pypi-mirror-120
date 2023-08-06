from .lib import settrade_open_api as soa
from threading import Thread, Event
import json

key_one_topic = "ONE_TOPIC"
key_two_topic = "TWO_TOPIC"

class Subscriber:
    def __init__(self, context, id, cb_func, topic1, topic2, on_message, parse_float_func, args):
        self._e = Event()

        def cpp_callback(result):
            try:
                result = json.loads(result)
                result = parse_float_func(result)
                on_message(result, self, *args)
            except Exception as e:
                print(e)
                self.stop()

        self._t = None

        def t_callback():
            key = cb_func(context, topic1, cpp_callback) if id == key_one_topic else cb_func(context, topic1, topic2, cpp_callback)
                       
            # wait event
            self._e.wait()
            # after kill event
            soa.unsubscribe(context["channel_id"], key)

        self._t = Thread(target=t_callback)

    def start(self):
        self._t.start()

    def stop(self):
        self._e.set()
        self._t.join()


class MQTTWebsocket:
    def __init__(self, context):
        self._context = context

    def subscribe_bid_offer(self, symbol, on_message, args=()):
        def parse_float(result):
            if result["is_success"]:
                for i in ["bid_price1", "bid_price2", "bid_price3", "bid_price4", "bid_price5", "ask_price1", "ask_price2", "ask_price3", "ask_price4", "ask_price5"]:
                    result["data"][i] = float(result["data"][i])
            return result

        return Subscriber(
            self._context, key_one_topic, soa.subscribe_bid_offer, symbol, None, on_message, parse_float, args
        )
        
    def subscribe_candlestick(self, symbol, interval, on_message, args=()):
        interval_list = ["1m", "3m", "5m", "10m", "15m", "30m", "60m", "1d", "1w", "1M"]

        if interval not in interval_list:
            raise ValueError(interval + " is invalid. Please choose " + str(interval_list))

        def parse_float(result):
            if result["is_success"]:
                for i in ["open", "high", "low", "close", "value"]:
                    result["data"][i] = float(result["data"][i])
            return result

        return Subscriber(
            self._context, key_two_topic, soa.subscribe_candlestick, symbol, interval, on_message, parse_float, args
        )
        
    def subscribe_price_info(self, symbol, on_message, args=()):
        def parse_float(result):
            if result["is_success"]:
                for i in ["high", "low", "last", "projected_open_price", "change", "total_value"]:
                    result["data"][i] = float(result["data"][i])
            return result

        return Subscriber(
            self._context, key_one_topic, soa.subscribe_price_info, symbol, None, on_message, parse_float, args
        )

    def subscribe_derivatives_order(self, account_no, on_message, args=()):
        def parse_float(result):
            if result["is_success"]:
                for i in ["price"]:
                    result["data"][i] = float(result["data"][i])
            return result

        return Subscriber(
            self._context, key_one_topic, soa.subscribe_derivatives_order, account_no, None, on_message, parse_float, args
        )

    def subscribe_equity_order(self, account_no, on_message, args=()):
        def parse_float(result):
            if result["is_success"]:
                for i in ["price"]:
                    result["data"][i] = float(result["data"][i])
            return result

        return Subscriber(
            self._context, key_one_topic, soa.subscribe_equity_order, account_no, None, on_message, parse_float, args
        )
