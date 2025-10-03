import re
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/calculate', methods=['POST','GET'])
def calculator() -> float:
    expression = request.args.get('expression', '')
    cnt = []
    cnt.append(expression.count('+'))
    cnt.append(expression.count('-'))
    cnt.append(expression.count('*'))
    cnt.append(expression.count('/'))

    res = 0
    if cnt[0] + cnt[1] + cnt[2] + cnt[3] != 1:
        return "Error: Only one operator is allowed."
    
    nums = re.split(r'[+\-*/]', expression)
    nums = [float(num) for num in nums]
    if len(nums) != 2:
        return "Error: Invalid expression format."
    
    if cnt[0] == 1:
        res = nums[0] + nums[1]
    elif cnt[1] == 1:
        res =  nums[0] - nums[1]
    elif cnt[2] == 1:
        res = nums[0] * nums[1]
    elif cnt[3] == 1:
        if nums[1] == 0:
            return "Error: Division by zero."
        res = nums[0] / nums[1]
    
    return jsonify({"result": f"the result is {res}"})
    
if __name__ == "__main__":
    app.run(debug=True)