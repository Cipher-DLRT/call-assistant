# USD per MTok, list prices (conservative — Sonnet 5 intro pricing ignored).
# Model IDs resolved per amendment A3; keys match app/loop/llm.py.
PRICES = {
    "claude-haiku-4-5": (1.00, 5.00),
    "claude-sonnet-5": (3.00, 15.00),
}


# Ceiling semantics (law 5): allow() is a pre-call gate on spend so far — the
# call that crosses the ceiling completes (its cost can't be known up front),
# every later call is refused. The overshoot is bounded by one call.
class CostMeter:
    def __init__(self, ceiling_usd):
        import math
        if not (math.isfinite(ceiling_usd) and ceiling_usd > 0):
            raise ValueError(f"ceiling must be finite and positive: {ceiling_usd}")
        self.__ceiling_usd = ceiling_usd
        self._spent = 0.0
        self._gate_calls = 0
        self._hint_calls = 0
        self._input_tokens = 0
        self._output_tokens = 0
        self._ceiling_hit = False

    @property
    def ceiling_usd(self):
        return self.__ceiling_usd

    @property
    def spent(self):
        return self._spent

    def add(self, kind, model, input_tokens, output_tokens,
            cache_write_tokens=0, cache_read_tokens=0):
        input_price, output_price = PRICES[model]
        if kind not in ("gate", "hint"):
            raise ValueError("kind must be 'gate' or 'hint'")
        # cache writes bill at 1.25x input, cache reads at 0.1x input
        cost = (input_tokens * input_price
                + cache_write_tokens * input_price * 1.25
                + cache_read_tokens * input_price * 0.10
                + output_tokens * output_price) / 1_000_000
        self._spent += cost
        self._input_tokens += input_tokens
        self._output_tokens += output_tokens
        if kind == "gate":
            self._gate_calls += 1
        else:
            self._hint_calls += 1
        return cost

    def allow(self):
        allowed = self._spent < self.__ceiling_usd
        if not allowed:
            self._ceiling_hit = True
        return allowed

    def summary(self):
        return {
            "gate_calls": self._gate_calls,
            "hint_calls": self._hint_calls,
            "input_tokens": self._input_tokens,
            "output_tokens": self._output_tokens,
            "total_usd": round(self._spent, 6),
            "ceiling_usd": self.__ceiling_usd,
            "ceiling_hit": self._ceiling_hit,
        }
