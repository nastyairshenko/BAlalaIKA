MORAL_SCHEMAS = {
  "mentorship": {  # наставник↔ученик
    "roles": ["teacher","student"],
    "conditions": {"teacher_to_student":[("Supportive",10)], "student_to_teacher":[("Trusting",10)]},
    "target": {"teacher":{"Supportive":20,"Responsible":15}, "student":{"Trusting":20,"Eager to learn":20}},
    "actions": ["give_guidance","encourage_growth","ask_reflection"]
  },
  "comradeship": {
    "roles":["teacher","student"],
    "conditions":{"teacher_to_student":[("Friendly",10)], "student_to_teacher":[("Friendly",8)]},
    "target":{"teacher":{"Friendly":20}, "student":{"Enthusiastic":20,"Friendly":20}},
    "actions":["icebreaker_question","contextual_smalltalk"]
  },
  "social_empathy": {
    "roles":["teacher","student"],
    "conditions":{"teacher_to_student":[("Supportive",10)]},
    "target":{"teacher":{"Supportive":15},"student":{"Confident":15,"Trusting":15}},
    "actions":["reflect_emotion","validate_feeling"]
  },
  "professional_help": {
    "roles":["teacher","student"],
    "conditions":{"teacher_to_student":[("Responsible",10)], "student_to_teacher":[("Respectful",10)]},
    "target":{"teacher":{"Responsible":20},"student":{"Focused":20,"Trusting":15}},
    "actions":["set_agenda","confirm_success_criteria"]
  },

  # 6 целевых схем под разговорный английский
  "teaching_warmup_smalltalk": {
    "roles":["teacher","student"],
    "conditions":{"teacher_to_student":[("Friendly",15),("Supportive",10)], "student_to_teacher":[("Trusting",10)]},
    "target":{"teacher":{"Supportive":20,"Friendly":20}, "student":{"Enthusiastic":20,"Friendly":20,"Trusting":20}},
    "actions":["icebreaker_question","contextual_smalltalk"]
  },
  "gentle_error_correction": {
    "roles":["teacher","student"],
    "conditions":{"teacher_to_student":[("Supportive",15)], "student_to_teacher":[("Respectful",10)]},
    "target":{"teacher":{"Supportive":20,"Responsible":15}, "student":{"Confident":25,"Eager to learn":20,"Trusting":20}},
    "actions":["recast_with_highlight","micro_drill_followup"]
  },
  "celebrate_milestone": {
    "roles":["teacher","student"],
    "conditions":{"teacher_to_student":[("Supportive",15)], "student_to_teacher":[("Eager to learn",10)]},
    "target":{"teacher":{"Praiseworthy":15}, "student":{"Confident":30,"Enthusiastic":25}},
    "actions":["badge_and_praise","level_up_prompt"]
  },
  "task_switch_and_flow": {
    "roles":["teacher","student"],
    "conditions":{"teacher_to_student":[("Supportive",10)], "student_to_teacher":[("Curious",10)]},
    "target":{"teacher":{"Responsible":15}, "student":{"Enthusiastic":20,"Focused":20}},
    "actions":["from_free_talk_to_roleplay","from_roleplay_to_feedback"]
  },
  "roleplay_partner": {
    "roles":["teacher","student"],
    "conditions":{"student_to_teacher":[("Eager to learn",10),("Playful",8)]},
    "target":{"student":{"Confident":25,"Fluent":20,"Enthusiastic":20}},
    "actions":["set_scene_and_goal","in_character_nudge"]
  },
  "micro_goal_and_brief": {
    "roles":["teacher","student"],
    "conditions":{"teacher_to_student":[("Responsible",10)], "student_to_teacher":[("Respectful",10)]},
    "target":{"teacher":{"Responsible":20}, "student":{"Focused":20,"Trusting":15}},
    "actions":["agree_on_15min_goal","confirm_success_criteria"]
  }
}
