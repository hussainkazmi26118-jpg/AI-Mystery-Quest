import os, json
from groq import Groq

class GroqService:
    def __init__(self):
        self.key = os.getenv("GROQ_API_KEY")
        self.available = bool(self.key)
        self.client = Groq(api_key=self.key) if self.available else None
        self.model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    def _complete(self, messages, temperature=0.7):
        if not self.available: return None
        try:
            response = self.client.chat.completions.create(
                model=self.model, messages=messages, temperature=temperature, max_tokens=1200
            )
            return response.choices[0].message.content.strip()
        except Exception:
            return None

    def generate_case(self, difficulty, theme):
        prompt = f"""Create a fair, solvable detective mystery in JSON. Difficulty: {difficulty}. Theme: {theme}.
Return ONLY JSON with keys title,difficulty,intro,location,incident,suspects,evidence,puzzle,hints,solution.
suspects: 3 objects with name,role,motive,alibi,statement.
evidence: 4 objects with name,description.
puzzle: object with title,description,answer.
hints: array of exactly 3 progressive hints.
solution: object with culprit and explanation.
Make culprit exactly one suspect name. Ensure evidence logically proves solution."""
        raw = self._complete([{"role":"system","content":"You design internally consistent mystery game cases. Output valid JSON only."},
                              {"role":"user","content":prompt}], 0.85)
        if not raw: return None
        try:
            data = json.loads(raw[raw.find("{"):raw.rfind("}")+1])
            required = ["title","intro","location","incident","suspects","evidence","puzzle","hints","solution"]
            if all(k in data for k in required) and len(data["suspects"]) >= 3 and len(data["evidence"]) >= 3:
                return data
        except Exception:
            pass
        return None

    def get_hint(self, case, level):
        return self._complete([
            {"role":"system","content":"You are a fair detective mentor. Do not reveal the culprit directly. Give one progressive hint."},
            {"role":"user","content":f"Case: {case['intro']} Evidence: {json.dumps(case['evidence'])} Level: {level}. Provide a concise hint."}
        ], 0.4)

    def chat(self, case, question, history):
        messages = [{"role":"system","content":"You are Detective AI, a helpful but spoiler-conscious investigation partner. Only use facts in this case. Do not reveal the culprit or hidden solution. Encourage evidence-based reasoning. Case facts: "+json.dumps({k:v for k,v in case.items() if k not in ("solution","answer_key")})}]
        messages.extend(history[-8:])
        messages.append({"role":"user","content":question})
        return self._complete(messages, 0.5)
