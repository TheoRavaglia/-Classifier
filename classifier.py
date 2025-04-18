import wx
import numpy as np

class SmileyClassifier(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Smiley Face Classifier", size=(400, 500))
        
        # Inicialização dos pesos
        self.weights = [0] * 25
        
        # Dados de exemplo
        self.samples = {
            'Happy': [
                [1,1,1,1,1,1,0,0,0,1,1,0,1,0,1,1,0,0,0,1,1,1,1,1,1],
                [1,1,0,1,1,1,0,0,0,1,0,0,1,0,0,1,0,0,0,1,1,1,0,1,1]
            ],
            'Sad': [
                [1,1,1,1,1,1,0,0,0,1,1,0,1,0,1,1,1,1,1,1,0,0,0,0,0],
                [1,1,0,1,1,1,0,0,0,1,0,0,1,0,0,1,1,1,1,1,0,0,0,0,0]
            ]
        }
        
        self.init_ui()
        
    def init_ui(self):
        panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Grade de pesos 5x5
        grid_sizer = wx.GridSizer(5, 5, 2, 2)
        self.weight_buttons = []
        for i in range(25):
            btn = wx.Button(panel, label=" ", size=(50, 50))
            btn.Bind(wx.EVT_BUTTON, lambda event, idx=i: self.toggle_weight(idx))
            grid_sizer.Add(btn, 0, wx.EXPAND)
            self.weight_buttons.append(btn)
            
        # Botão de teste
        self.test_btn = wx.Button(panel, label="Test Classifier")
        self.test_btn.Bind(wx.EVT_BUTTON, lambda event: self.test_classifier())
        
        # Layout
        main_sizer.Add(grid_sizer, 1, wx.ALL | wx.EXPAND, 10)
        main_sizer.Add(self.test_btn, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        panel.SetSizer(main_sizer)
        
    def toggle_weight(self, idx):
        """Alterna entre 1, -1 e 0"""
        if self.weights[idx] == 0:
            self.weights[idx] = 1
            self.weight_buttons[idx].SetBackgroundColour(wx.Colour(0, 255, 0))  # Verde
        elif self.weights[idx] == 1:
            self.weights[idx] = -1
            self.weight_buttons[idx].SetBackgroundColour(wx.Colour(255, 0, 0))  # Vermelho
        else:
            self.weights[idx] = 0
            self.weight_buttons[idx].SetBackgroundColour(wx.NullColour)
            
        self.weight_buttons[idx].Refresh()
        
    def predict(self, inputs):
        """Faz a predição"""
        linear = sum(w * i for w, i in zip(self.weights, inputs))
        return 1 if linear > 0 else -1
        
    def test_classifier(self):
        """Testa o classificador"""
        results = {'Happy': {'correct': 0, 'total': 0},
                  'Sad': {'correct': 0, 'total': 0}}
                  
        for label, samples in self.samples.items():
            for sample in samples:
                prediction = self.predict(sample)
                true_label = 1 if label == 'Happy' else -1
                
                if prediction == true_label:
                    results[label]['correct'] += 1
                results[label]['total'] += 1
                
        # Mostra resultados
        msg = (f"Results:\nHappy: {results['Happy']['correct']}/{results['Happy']['total']}\n"
              f"Sad: {results['Sad']['correct']}/{results['Sad']['total']}")
        wx.MessageBox(msg, "Results", wx.OK | wx.ICON_INFORMATION)

if __name__ == "__main__":
    app = wx.App()
    frame = SmileyClassifier()
    frame.Show()
    app.MainLoop()