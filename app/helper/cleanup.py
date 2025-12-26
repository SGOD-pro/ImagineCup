import re
def parse_range(range_str: str):
    if not range_str:
        return None, None

    nums = re.findall(r"\d+(?:\.\d+)?", range_str)
    print("nums:", nums)

    if len(nums) >= 2:
        return float(nums[0]), float(nums[1])

    return None, None

def normalize_labs(tests: list[dict]) -> list[dict]:
    normalized = []

    for t in tests:
          print(t)
          value = t.get("value")
          rr = t.get("reference_range")

          low, high = (None, None)
          status = "UNKNOWN"

          if value is not None and rr:
               low, high = parse_range(rr)

               if low is not None and high is not None:
                    if value < low:
                         status = "LOW"
                    elif value > high:
                         status = "HIGH"
                    else:
                         status = "NORMAL"

          normalized.append({
               **t,
               "reference_low": low,
               "reference_high": high,
               "status": status
          })

    return normalized
