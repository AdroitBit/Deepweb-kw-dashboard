from tempo.serve.utils import pipeline, pipeline_context, predictmethod, deploy

@pipeline(name="my_pipeline")
class MyPipeline:
    @predictmethod
    def predict(self, data: str) -> str:
        # Add your data processing or ML model inference logic here
        return data.upper()

# Deploy the pipeline
my_pipeline = MyPipeline()
deploy(my_pipeline)
