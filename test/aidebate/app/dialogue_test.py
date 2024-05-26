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
        supported_with_install = []
        soon_to_be_supported = []
        for model_id, model_type in get_chat_model_mappings().items():
            model_type_full_name = str(model_type)[8:-2]
            model_description = f"{model_id} ({model_type_full_name})"
            try:
                kwargs = {'provider': model_id, f'{model_id}_api_key': 'test'}
                dialogue_agent_provider.get_chat_model(**kwargs)
                supported.append(model_description)
            except ImportError:
                supported_with_install.append(model_id)
            except Exception as ex:
                print(f"Error creating model '{model_description}':\n{type(ex)}")
                soon_to_be_supported.append(model_description)

        DialogueTestCase.__save_supported_models(
            supported, supported_with_install, soon_to_be_supported)

    @staticmethod
    def __save_supported_models(supported: [str], supported_with_install,
                                soon_to_be_supported: [str]):
        output = "# Supported Models"
        output = DialogueTestCase.__add_models(
            output, "Supported by default:", supported)
        output = DialogueTestCase.__add_models(
            output, "Supported, but additional package(s) need to be installed. "
                    "E.g. for `anthropic` install `langchain-anthropic`.", supported_with_install)
        output = DialogueTestCase.__add_models(
            output, "Will soon be supported:", soon_to_be_supported)

        print(f"{'*'*50}\nUpdating {supported_models_file}\n{'*'*50}")
        write_content(output, supported_models_file)

    @staticmethod
    def __add_models(add_to: str, sub_heading: str, models: [str]) -> str:
        supported = '\n'.join([f'* {model}' for model in models])
        return f"{add_to}\n\n### {sub_heading}\n\n{supported}"


if __name__ == "__main__":
    unittest.main()
