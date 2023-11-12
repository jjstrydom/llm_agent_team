from langchain.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.prompts import PromptTemplate
from response_components import ResponseComponent, project_plan_components, task_outline_components
from llm_output_parser import extract_tasks_content
from storage import text_to_parquet

class BaseAgent(object):
    def __init__(self, model:str='llama2'):
        self.emotive_prompt = "\nThis is very important for my career."
        self.model = model
        self.update_model(model)

    def update_model(self, model:str):
        self.__model = Ollama(
            model=model, callback_manager=CallbackManager([StreamingStdOutCallbackHandler()])
        )

    def prompt(self, prompt:str):
        return self.__model(prompt)


class PMAgent(BaseAgent):
    def __init__(self, project_brief:str):
        super().__init__(model='agent_pm')
        self.update_project_brief(project_brief)

    def clear_plans(self):
        self.project_plan_md = None
        self.project_plan = None
        self.task_plan_md = None
        self.task_plan = None

    def update_project_brief(self, project_brief:str):
        self.project_brief = project_brief
        self.clear_plans()

    @staticmethod
    def structured_output_instructions_from_response_components(response_components: list[ResponseComponent]):
        base_instruction = "The output should be a markdown code snippet formatted in the following schema:\n"
        for n, response_component in enumerate(response_components):
            base_instruction += f"{n+1}. A markdown heading (#) with the title {response_component.name}, followed by a desciption of {response_component.description} as a {response_component.output_format}.\n"
        return base_instruction

    def generate_project_plan(self):

        response_format = self.structured_output_instructions_from_response_components(project_plan_components)
        
        
        template_list = ["You have been given the following project brief. Identify and plan the key project tasks step by step.\n",
            "{format_instructions}\n",
            "Project Brief:\n",
            "{brief}\n",
            "{emotive_prompt}\n",
        ]
        template = ''.join(template_list)

        prompt = PromptTemplate(
            template=template,
            input_variables=["brief", "emotive_prompt"],
            partial_variables={"format_instructions": response_format}
        )

        _input = prompt.format_prompt(brief=self.project_brief, emotive_prompt=self.emotive_prompt)
        self.project_plan_md = super().prompt(_input.to_string())
        self.response_components = project_plan_components
        return self.project_plan_md
    
    def parse_project_plan(self):
        self.project_plan = extract_tasks_content(self.project_plan_md, self.response_components)
        return self.project_plan
    
    def generate_task_breakdown(self):
        response_format = self.structured_output_instructions_from_response_components(task_outline_components)

        template_list = [
            "Given the following project brief, and a list of tasks to solve for the brief. Take each task in the list and plan it step by step in detail.\n",
            "{format_instructions}\n",
            "Project Brief:\n",
            "{brief}\n",
            "Tasks:\n",
            "{tasks}\n",
            "{emotive_prompt}\n",
        ]
        template = ''.join(template_list)
        prompt = PromptTemplate(
            template=template,
            input_variables=["brief", "tasks", "emotive_prompt"],
            partial_variables={"format_instructions": response_format}
        )

        _input = prompt.format_prompt(brief=self.project_brief, tasks=self.project_plan['tasks'], emotive_prompt=self.emotive_prompt)
        task_plan = super().prompt(_input.to_string())
        return task_plan


if __name__ == '__main__':
    import traceback
    brief = """\
- The project is for a big multinational firm.
- The firm employs about 10000 people.
- The firm is grouped into a hierarchical structure, where each group specialises in a different industry or competency.
- The firm is struggling to forecast its revenue accurately for one of the competencies.
- We are proposing to use machine learning and algorithms coupled with sourcing external market data to improve forecasting.
- We aim to achieve a better accuracy than their current forecasting process.
"""
    counter = 0
    while True:
        try:
            counter += 1
            print('\n', counter, '='*90)
            pm_agent = PMAgent(project_brief=brief)
            project_plan = pm_agent.generate_project_plan()
            text_to_parquet('data/project_plan.parquet', project_plan)
            project_plan_parsed = pm_agent.parse_project_plan()
            print('\n', counter, '-'*10)
            task_outline = pm_agent.generate_task_breakdown()
            text_to_parquet('data/task_outline.parquet', task_outline)
            print('\n', counter, '='*90)
        except Exception as e:
            print('\n', "ERROR - "*10)
            print(traceback.format_exc())
            print('\n', "ERROR - "*10)
