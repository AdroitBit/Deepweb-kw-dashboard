import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
print(os.getcwd())


#Copy from server_api.schema to deepweb_puller.schema
f_source = open("server_api/schema.py", "r")
f_target = open("deepweb_puller/schema.py", "w")
f_target.write(f_source.read())
f_source.close()



import server_api.schema as schema
from pydantic import BaseModel
import inspect



interface_contents=[]
for var in dir(schema):
    if var.startswith("__"):
        continue
    var_value:BaseModel= getattr(schema,var)
    if not inspect.isclass(var_value):
        continue
    if var_value==BaseModel:
        continue
    # print(var, var_value,issubclass(var_value,BaseModel))
    if issubclass(var_value, BaseModel):
        schema_dict=var_value.schema()
        # print(schema_dict)

        contents=[]
        for field in schema_dict["properties"]:
            line=""
            line+="    "
            line+=field
            line+="" if field in schema_dict["required"] else "?"
            line+=": "
            if "$ref" in schema_dict['properties'][field]:
                raise NotImplementedError("Not implemented yet")
            else:
                if schema_dict['properties'][field]['type']=="integer":
                    line+="number"
                elif schema_dict['properties'][field]['type']=="array":
                    raise NotImplementedError("Not implemented yet")
                elif schema_dict['properties'][field]['type']=="enum":
                    raise NotImplementedError("Not implemented yet")
                else:
                    line+=schema_dict['properties'][field]['type']
            line+=";"
            contents.append(line)


        content="\n".join(contents)
        
        interface_content=open("interface_format.ts","r").read()
        interface_content=interface_content.replace("SCHEMA_TITLE",schema_dict["title"])
        interface_content=interface_content.replace("SCHEMA_CONTENT",content)

        interface_contents.append(interface_content)

interface_file_content="\n\n".join(interface_contents)

print(interface_file_content)

with open(f"antd_deepweb_dashboard/src/schemas/schema.ts","w") as f:
    f.write(interface_file_content)

# import pydantic2ts
# pydantic2ts.generate_typescript_defs(schema, "antd_deepweb_dashboard/src/schema.ts")
