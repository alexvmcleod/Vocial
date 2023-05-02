import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

import warnings
from transformers import logging as transformers_logging

warnings.filterwarnings("ignore")
transformers_logging.set_verbosity(transformers_logging.ERROR)

class LabelModel:
    def __init__(self):
        self.modelpaths = {"time":"models/time.pt","stat":None,"metric":"models/metric.pt"}
        self.max_length = 128
        self.tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)

        self.label_map_time = {
            0: 'recent',
            1: 'hour',
            2: 'day',
            3: 'week',
            4: 'month',
            5: 'year',
        } 

        self.label_map_metric = {
            0: 'reactions',
            1: 'comments',
            2: 'forwards',
            3: 'views',
            4: 'followers',
        }


        self.label_map_stat = {
            0: 'top',
            1: 'average',
            2: 'median',
            3: 'bottom',
        }

        self.label_maps = {
            "time":self.label_map_time,
            "metric":self.label_map_metric,
            "stat":self.label_map_stat,
        }

    def load_model(self, model_path):
        model = AutoModelForSequenceClassification.from_pretrained('bert-base-uncased',num_labels=5)
        state_dict = torch.load(model_path)
        model.load_state_dict(state_dict)
        model.eval()
        return model
    
    def preprocess_input(self, input_string, tokenizer, max_length):
        tokens = tokenizer.tokenize(input_string)
        tokens = tokens[:max_length] + ['<PAD>'] * (max_length - len(tokens))
        token_indices = tokenizer.convert_tokens_to_ids(tokens)
        input_tensor = torch.tensor(token_indices).unsqueeze(0)  # Add batch dimension
        return input_tensor
    
    def perform_inference(self, model, input_tensor):
        with torch.no_grad():
            output = model(input_tensor)
        return output.logits

    def postprocess_output(self, output_tensor, label_map):
        predicted_index = torch.argmax(output_tensor, dim=1).item()
        predicted_label = label_map[predicted_index]
        return predicted_label
    
    def main(self,message):
        finallabels = {"time":"NONE","stat":"NONE","metric":"NONE"}
        
        for category in self.modelpaths:
            # print(f"{category} THINF")
            #print(self.modelpaths[category])

            if self.modelpaths[category]:
                thingy = self.modelpaths[category]
                model = self.load_model(thingy)
                input_tensor = self.preprocess_input(message, self.tokenizer, self.max_length)
                output_tensor = self.perform_inference(model, input_tensor)
                predicted_label = self.postprocess_output(output_tensor, self.label_maps[category])
                finallabels[category] = predicted_label
            else:
                #runs if no model availible
                predicted_label
                finallabels[category] = self.label_maps[category][0]
        print(finallabels)
        return finallabels

if __name__ == "__main__":
    x = LabelModel()
    print(x.main("what posts gave the most reactions in the last month"))