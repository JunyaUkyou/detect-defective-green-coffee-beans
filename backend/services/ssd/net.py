# パッケージインポート
import torch
import torchvision
import torch.nn.functional as F
import pytorch_lightning as pl
from torchvision.models.detection import ssd300_vgg16, SSD300_VGG16_Weights
from torchvision.models.detection.ssd import SSDClassificationHead
from torchvision.models.detection._utils import retrieve_out_channels

# 別ファイルからインポート
from .constants import CLASS_NAMES, IOU_THRESHOLD, SCORE_THRESHOLD

class Net(pl.LightningModule):

    def __init__(self):
        super().__init__()
        # torchvision.models.detection.ssd300_vgg16
        model = ssd300_vgg16(weights=SSD300_VGG16_Weights.DEFAULT)

        # 分類結果を出力する箇所の入れ替え
        in_channels = retrieve_out_channels(model.backbone, (300, 300))  #　入力のチャンネル数
        num_anchors = model.anchor_generator.num_anchors_per_location()  # アンカーの数
        num_classes=len(CLASS_NAMES)+1  # 分類数: 背景も含めて分類するため1を加える
        model.head.classification_head = SSDClassificationHead(in_channels, num_anchors, num_classes)


        # すべてのパラメータを凍結
        for param in model.parameters():
            param.requires_grad = False

        # classification_headのパラメータのみ更新可能に
        for param in model.head.classification_head.parameters():
            param.requires_grad = True

        self.ssd300 = model

    def forward(self, x, t=None):
        if self.training:
            return self.ssd300(x, t)
        else:
            outputs = self.ssd300(x)

            # NMSの適用
            for i in range(len(outputs)):
                boxes = outputs[i]['boxes']
                scores = outputs[i]['scores']
                labels = outputs[i]['labels']

                # IoU閾値でNMSを適用
                keep = torchvision.ops.nms(boxes, scores, iou_threshold=IOU_THRESHOLD)

                # NMS後のボックス、スコア、ラベルを残す
                boxes = boxes[keep]
                scores = scores[keep]
                labels = labels[keep]

                # スコアしきい値を適用して、低スコアのバウンディングボックスを除去
                score_keep = scores >= SCORE_THRESHOLD

                # NMS後のボックス、スコア、ラベルを残す
                outputs[i]['boxes'] = boxes[score_keep]
                outputs[i]['scores'] = scores[score_keep]
                outputs[i]['labels'] = labels[score_keep]

            return outputs

    def training_step(self, batch, batch_idx):
        x, t = batch
        losses = self(x, t)
        loss = sum(losses.values())
        self.log('train_loss', loss, on_step=True, on_epoch=True, prog_bar=True)
        return loss

    def configure_optimizers(self):
        params = [p for p in self.ssd300.parameters() if p.requires_grad]
        optimizer = torch.optim.Adam(params)
        scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.5)
        return [optimizer], [scheduler]