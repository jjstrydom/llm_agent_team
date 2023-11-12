from pydantic import BaseModel

class ResponseComponent(BaseModel):
    name: str
    description: str
    output_format: str

tasks = ResponseComponent(
        name="tasks",
        description="the project split into tasks",
        output_format="markdown list",
    )
task_breakdown = ResponseComponent(
    name="task breakdown",
    description="the detailed step by step breakdown of each task",
    output_format="markdown list",
)
timeline = ResponseComponent(
        name="timeline",
        description="the time required for each task",
        output_format="markdown list",
    )
deliverables =  ResponseComponent(
        name="deliverables",
        description="the project deliverables",
        output_format="markdown list",
    )
team = ResponseComponent(
        name="team",
        description="the required team's skills and experience level to deliver the project",
        output_format="markdown list",
    )
risks = ResponseComponent(
        name="risks",
        description="the project risks",
        output_format="markdown list",
    )
budget = ResponseComponent(
        name="budget",
        description="the budget required to deliver each task",
        output_format="markdown list",
    )
metrics = ResponseComponent(
        name="metrics",
        description="the project metrics to measure success against",
        output_format="markdown list",
    )

project_plan_components = [tasks, task_breakdown, timeline, deliverables, team, risks, budget, metrics]
task_outline_components = [task_breakdown]