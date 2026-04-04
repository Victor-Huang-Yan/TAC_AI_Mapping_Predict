from sentence_transformers import SentenceTransformer, InputExample, losses
from torch.utils.data import DataLoader
import pandas as pd

# 加载预训练模型
model = SentenceTransformer('all-MiniLM-L6-v2')

# 加载训练数据
train_data = pd.read_csv('train_data.csv')

# 转换为InputExample格式
train_examples = []
for _, row in train_data.iterrows():
    train_examples.append(InputExample(
        texts=[row['sentence1'], row['sentence2']],
        label=float(row['score'])
    ))

# 创建数据加载器
train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=16)

# 定义损失函数
train_loss = losses.CosineSimilarityLoss(model)

# 微调模型
model.fit(
    train_objectives=[(train_dataloader, train_loss)],
    epochs=3,  # 训练轮次，可根据数据量调整
    warmup_steps=100,  # 预热步骤，帮助模型稳定训练
    output_path='models/fine-tuned-all-MiniLM-L6-v2'  # 保存路径
)

print("微调完成！模型已保存到 'models/fine-tuned-all-MiniLM-L6-v2'")