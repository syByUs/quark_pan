import json

import lark_oapi as lark
from lark_oapi.api.bitable.v1 import *

CONFIT_TABLE = {
    "quark_resource": {
        "app_token": "<feishu_app_token>",
        "table_id": "<feishu_table_id>",
        "view_id": "veweC5hkpI",
        "field_names": ["夸克分享链接", "已转存"],
        "automatic_fields": False
    }
}
# SDK 使用说明: https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/server-side-sdk/python--sdk/preparations-before-development
# 以下示例代码默认根据文档示例值填充，如果存在代码问题，请在 API 调试台填上相关必要参数后再复制代码使用
# 复制该 Demo 后, 需要将 "YOUR_APP_ID", "YOUR_APP_SECRET" 替换为自己应用的 APP_ID, APP_SECRET.
class FeishuQuarkResourceManager:
    def __init__(self):
        app_id = "<feishu_app_id>"
        app_secret = "<feishu_app_secret>"
        quark_resource = CONFIT_TABLE.get("quark_resource")
        app_token = quark_resource.get("app_token")
        table_id = quark_resource.get("table_id")
        view_id = quark_resource.get("view_id")
        field_names = quark_resource.get("field_names")

        self.app_token = app_token
        self.table_id = table_id
        self.view_id = view_id
        self.field_names = field_names
        self.client = lark.Client.builder() \
            .app_id(app_id) \
            .app_secret(app_secret) \
            .log_level(lark.LogLevel.DEBUG) \
            .build()
        
    # 更新表格 todo
    def update_table_record(self, record_id):
        # 构造请求对象
        fields = {"已转存" : "1"}
        request: UpdateAppTableRecordRequest = UpdateAppTableRecordRequest.builder() \
            .app_token(self.app_token) \
            .table_id(self.table_id) \
            .record_id(record_id) \
            .user_id_type("open_id") \
            .ignore_consistency_check(True) \
            .request_body(AppTableRecord.builder()
                .fields(fields=fields)
                .build()) \
            .build()

        # 发起请求
        response: UpdateAppTableRecordResponse = self.client.bitable.v1.app_table_record.update(request)

        # 处理失败返回
        if not response.success():
            lark.logger.error(
                f"client.bitable.v1.app_table_record.update failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
            return

        # 处理业务结果
        lark.logger.info(lark.JSON.marshal(response.data, indent=4))
        print("更新成功")

    def search_table_record(self):
        request: SearchAppTableRecordRequest = SearchAppTableRecordRequest.builder() \
        .app_token(self.app_token) \
        .table_id(self.table_id) \
        .page_size(20) \
        .request_body(SearchAppTableRecordRequestBody.builder()
            .view_id(self.view_id)
            .field_names(self.field_names)
            .filter(FilterInfo.builder()
                .conjunction("and")
                .conditions([Condition.builder()
                    .field_name("已转存")
                    .operator("is")
                    .value(["0"])
                    .build()])
                .build())
            .automatic_fields(False)
            .build()) \
        .build()

        # 发起请求
        response: SearchAppTableRecordResponse = self.client.bitable.v1.app_table_record.search(request)

        # 处理失败返回
        if not response.success():
            lark.logger.error(
                f"client.bitable.v1.app_table_record.search failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
            return

        # 处理业务结果
        # lark.logger.info(lark.JSON.marshal(response.data, indent=4))
        data = response.data
        items = data.items
        new_items = []
        for item in items:
            fields = item.fields
            quark_share_link = fields.get("夸克分享链接")[0].get("text")
            record_id = item.record_id
            new_items.append({"quark_share_link": quark_share_link, "record_id": record_id})
        print(new_items)
        return new_items

def main():
    # 创建client
    client = lark.Client.builder() \
        .app_id("<feishu_app_id>") \
        .app_secret("<app_secret>") \
        .log_level(lark.LogLevel.DEBUG) \
        .build()


    # 构造请求对象
    quark_resource = CONFIT_TABLE.get("quark_resource")
    app_token = quark_resource.get("app_token")
    table_id = quark_resource.get("table_id")
    view_id = quark_resource.get("view_id")
    field_names = quark_resource.get("field_names")
    request: SearchAppTableRecordRequest = SearchAppTableRecordRequest.builder() \
        .app_token(app_token) \
        .table_id(table_id) \
        .page_size(20) \
        .request_body(SearchAppTableRecordRequestBody.builder()
            .view_id(view_id)
            .field_names(field_names)
            .sort([Sort.builder()
                .field_name("URL")
                .desc(True)
                .build()
                ])
            .filter(FilterInfo.builder()
                .conjunction("and")
                .conditions([Condition.builder()
                    .field_name("已转存")
                    .operator("is")
                    .value(["0"])
                    .build()
                    ])
                .build())
            .automatic_fields(False)
            .build()) \
        .build()

    # 发起请求
    response: SearchAppTableRecordResponse = client.bitable.v1.app_table_record.search(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.bitable.v1.app_table_record.search failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
        return

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))


if __name__ == "__main__":
    # main()

    manager = FeishuQuarkResourceManager()
    # manager.search_table_record()
    manager.update_table_record("recuOP8PegGAvj")