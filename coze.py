import os
import time
from cozepy import COZE_CN_BASE_URL, Coze, TokenAuth, WorkflowExecuteStatus

class CozeManager:
    def __init__(self, workflow_id):
        """
        初始化 CozeManager
        
        Args:
            workflow_id (str): Coze 工作流的 ID
        """
        self.coze_api_token = '替换成你自己的coze_api_token'
        self.coze_api_base = COZE_CN_BASE_URL
        self.coze = Coze(auth=TokenAuth(token=self.coze_api_token), base_url=self.coze_api_base)
        self.workflow_id = workflow_id  # 从外部传入 workflow_id

    def run_workflow(self, parameters={}, is_async=False):
        """
        运行 Coze 工作流，接受一个文本参数作为输入。
        """
        print("run_workflow", self.workflow_id, parameters)
        workflow = self.coze.workflows.runs.create(
            workflow_id=self.workflow_id,
            parameters=parameters,
            is_async=is_async
        )
        print("workflow.data:", workflow.data, "workflow.debug_url:", workflow.debug_url, "workflow.execute_id:", workflow.execute_id)
        return workflow.data, workflow.debug_url, workflow.execute_id

    def retrieve_workflow_result(self, execute_id):
        while True:
            run_history = self.coze.workflows.runs.run_histories.retrieve(workflow_id=self.workflow_id, execute_id=execute_id)
            if run_history.execute_status == WorkflowExecuteStatus.FAIL:
                raise Exception(f"Workflow execution failed: {run_history.error_message}")
            elif run_history.execute_status == WorkflowExecuteStatus.SUCCESS:
                print("Workflow execution success:", run_history.output)
                return run_history.output
            elif run_history.execute_status == WorkflowExecuteStatus.RUNNING:
                print("Workflow execution running:", run_history)
                time.sleep(5)
                continue
            else:
                time.sleep(2)
                raise Exception(f"Workflow execution failed: {run_history.error_message}")

if __name__ == "__main__":
    # 示例：从外部传入 workflow_id
    workflow_id = '替换你自己的工作流ID'  # 替换为实际的 workflow_id
    manager = CozeManager(workflow_id)
    manager.run_workflow("思移力")