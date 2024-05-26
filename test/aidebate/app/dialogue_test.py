import os
import unittest

from pyu.io.file import write_content

from aidebate.app.dialogue import get_chat_model_mappings, DialogueAgentProvider

supported_models_file = os.path.join("docs", "supported-models.md")


class DialogueTestCase(unittest.TestCase):
    @staticmethod
    def test_supported_models():
        dialogue_agent_provider: DialogueAgentProvider = DialogueAgentProvider()
        supported = []
        soon_to_be_supported = []
        for model_id, model_type in get_chat_model_mappings().items():
            model_type_full_name = str(model_type)[8:-2]
            model_description = f"{model_id} ({model_type_full_name})"
            try:
                kwargs = {'provider': model_id, f'{model_id}_api_key': 'test'}
                dialogue_agent_provider.get_chat_model(**kwargs)
                supported.append(model_description)
            except ImportError as ex:
                print(f"I believe we support model '{model_description}': {type(ex)}, "
                      f"you just have install it with: pip install {model_id}")
                supported.append(model_description)
            except Exception as ex:
                print(f"Error creating model '{model_description}': {type(ex)}")
                soon_to_be_supported.append(model_description)
        DialogueTestCase.__save_supported_models(supported, soon_to_be_supported)

    @staticmethod
    def __save_supported_models(supported: [str], soon_to_be_supported: [str]):
        output = "# Supported Models\n\n### The following chat models are supported:\n\n"
        supported = '\n'.join([f'* {model}' for model in supported])
        output = f"{output}{supported}"
        output = f"{output}\n\n### The following chat models will soon be supported:\n\n"
        soon_to_be_supported = '\n'.join([f'* {model}' for model in soon_to_be_supported])
        output = f"{output}{soon_to_be_supported}"

        write_content(output, supported_models_file)


if __name__ == "__main__":
    unittest.main()
