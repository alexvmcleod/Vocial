import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

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

        self.label_maps = {
            "time":self.label_map_metric,
            "metric":self.label_map_metric,
        }
        
    def generate_labels(self,message):
        #TODO
        pass

    def load_model(self,model_path):
        model = torch.load(model_path)
        model.eval()
        return model
    
    def preprocess_input(self, input_string, tokenizer, max_length):
        tokens = tokenizer.tokenize(input_string)
        tokens = tokens[:max_length] + ['<PAD>'] * (max_length - len(tokens))
        token_indices = tokenizer.convert_tokens_to_ids(tokens)
        input_tensor = torch.tensor(token_indices).unsqueeze(0)  # Add batch dimension
        return input_tensor
    
    def perform_inference(model, input_tensor):
        with torch.no_grad():
            output_tensor = model(input_tensor)
        return output_tensor

    def postprocess_output(output_tensor, label_map):
        predicted_index = torch.argmax(output_tensor, dim=1).item()
        predicted_label = label_map[predicted_index]
        return predicted_label
    
    def main(self,message):
        finallabels = {"time":"NONE","stat":"NONE","metric":"NONE"}
        
        for category in self.modelpaths:
            print(f"{category} THINF")
            #print(self.modelpaths[category])

            if self.modelpaths[category]:
                thingy = self.modelpaths[category]
                model = self.load_model(thingy)
                input_tensor = self.preprocess_input(message, self.tokenizer, self.max_length)
                output_tensor = self.perform_inference(model, input_tensor)
                predicted_label = self.postprocess_output(output_tensor, self.label_maps[category])
                finallabels[category] = predicted_label
                print(predicted_label)
        return finallabels

        # model = self.load_model(model_path)

        # input_string = "Your input string goes here"
        # max_length = 128  # Adjust this according to your model's requirements

        # input_tensor = preprocess_input(input_string, tokenizer, max_length)
        # output_tensor = perform_inference(model, input_tensor)
        # predicted_label = postprocess_output(output_tensor, label_map)

if __name__ == "__main__":
    x = LabelModel()
    x.main("what post gave the most reactions in the last year")