from .schema_manager import SchemaManager
from .policy_router import ACTION_PRESETS
from ..core.deepseek_interface import LLMClient

class VirtualTutor:
    def __init__(self, llm: LLMClient | None = None):
        self.llm = llm or LLMClient()
        self.stage = 1  # 1..4
        self.manager = SchemaManager()
        self.success_counter = 0

    async def reply(self, user_text: str, vad: list[float], meta: dict) -> str:
        bored = bool(meta.get("bored"))
        success = self._auto_success(user_text)
        schema, action = self.manager.select({"stage": self.stage, "vad": vad, "flags": {"bored": bored, "success": success}})

        topic = meta.get("topic")
        force_roleplay = bool(meta.get("force_roleplay"))

        sys = {"role": "system", "content": open("src/core/prompts/system_base.md", "r", encoding="utf-8").read()}
        instr = ACTION_PRESETS.get(action, "")

        # усиливаем инструкцию темой, если есть
        if topic:
            instr = f"Topic: {topic}\n{instr}"

        # по команде - принудительно сцена
        if force_roleplay:
            action = "set_scene_and_goal"
            instr = f"Topic: {topic or 'General'}\nStart a 3–5 min roleplay. Set the scene in one sentence, define the goal, then ask the student to begin."

        messages = [
            sys,
            {"role": "user", "content": f"Student says: {user_text}"},
            {"role": "system", "content": f"Active schema: {schema}. Action: {action}. Instruction: {instr}"}
        ]
        answer = await self.llm.chat(messages)
        self._update_stage(success, bored)
        return answer

    def _auto_success(self, txt: str) -> bool:
        # наивная эвристика «достигнута микро-цель»: длинный ответ + нет грубых ошибок (условно)
        return len(txt.split()) >= 15

    def _update_stage(self, success: bool, bored: bool):
        if bored and self.stage in (2,3): return  # держим сцену ролеплея в рамках шага
        if success:
            self.success_counter += 1
            if self.success_counter >= 3 and self.stage < 4:
                self.stage += 1
                self.success_counter = 0
