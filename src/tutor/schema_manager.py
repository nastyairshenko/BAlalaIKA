from .moral_schemas import MORAL_SCHEMAS

class SchemaManager:
    def __init__(self): self.schemas = MORAL_SCHEMAS

    def select(self, context: dict) -> tuple[str, str]:
        """
        Возвращает (schema_name, action) на основе контекста:
        context = { "stage": int, "vad": [v,a,d], "flags": {"bored":bool,"success":bool} }
        """
        stage = context.get("stage",1)
        v,a,d = context.get("vad",[0,0,0])
        bored = context.get("flags",{}).get("bored",False)
        success = context.get("flags",{}).get("success",False)

        if stage == 1:
            schema = "teaching_warmup_smalltalk"
            action = "contextual_smalltalk" if a < 0.2 else "icebreaker_question"
        elif stage in (2,3):
            if bored: schema, action = "task_switch_and_flow", "from_free_talk_to_roleplay"
            else:     schema, action = "gentle_error_correction", "recast_with_highlight"
        else:
            schema = "celebrate_milestone" if success else "professional_help"
            action = "badge_and_praise" if success else "confirm_success_criteria"
        return schema, action
