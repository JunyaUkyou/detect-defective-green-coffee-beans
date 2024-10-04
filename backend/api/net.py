import torch
import torchvision
import torchmetrics
import torch.nn.functional as F
import pytorch_lightning as pl
from torchvision import transforms
from torchvision.models.detection.ssd import SSDClassificationHead
from torchvision.models.detection._utils import retrieve_out_channels

class Net(pl.LightningModule):

    def __init__(self):
        super().__init__()
        model = torchvision.models.detection.ssd300_vgg16(pretrained=True)

        class_names = {
          1:"Good Bean (Front)",
          2:"Good Bean (Back)",
          3:"Defective Bean (Front, Shape Defect)",
          4:"Defective Bean (Back, Shape Defect)",
        }

        # 分類結果を出力する箇所の入れ替え
        in_channels = retrieve_out_channels(model.backbone, (300, 300))  #　入力のチャンネル数
        num_anchors = model.anchor_generator.num_anchors_per_location()  # アンカーの数
        num_classes=len(class_names)+1  # 分類数: 背景も含めて分類するため1を加える
        model.head.classification_head = SSDClassificationHead(in_channels, num_anchors, num_classes)


        # すべてのパラメータを凍結
        for param in model.parameters():
            param.requires_grad = False

        # classification_headのパラメータのみ更新可能に
        for param in model.head.classification_head.parameters():
            param.requires_grad = True

        self.ssd300 = model

        # mAP metricの初期化
        self.map_metric = torchmetrics.detection.MeanAveragePrecision()

    def forward(self, x, t=None):
        if self.training:
            return self.ssd300(x, t)
        else:
            outputs = self.ssd300(x)

            # しきい値を設定
            iou_threshold = 0.5
            score_threshold = 0.5
            # NMSの適用
            for i in range(len(outputs)):
                boxes = outputs[i]['boxes']
                scores = outputs[i]['scores']
                labels = outputs[i]['labels']

                # NMS適用前のインデックス数
                # (検出されたbbox数, 座標（x1, y1, x2, y2）)
                total_count = boxes.shape[0]

                # IoU閾値0.5でNMSを適用
                keep = torchvision.ops.nms(boxes, scores, iou_threshold=iou_threshold)

                # NMS適用前後のインデックス数を記録
                #print(f'Batch {i}: NMS 適用前:{total_count}  適用後:{len(keep)}')

                # NMS後のボックス、スコア、ラベルを残す
                boxes = boxes[keep]
                scores = scores[keep]
                labels = labels[keep]

                # スコアしきい値を適用して、低スコアのバウンディングボックスを除去
                score_keep = scores >= score_threshold

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

    def validation_step(self, batch, batch_idx):
        x, t = batch
        ## mAPの算出
        outputs = self(x)
        self.map_metric.update(outputs, t)
        return outputs

    def on_validation_epoch_end(self):
        # mAPの各値を個別にログ
        map_metrics = self.map_metric.compute()
        self.log('val_map', map_metrics['map'])
        self.log('val_map_50', map_metrics['map_50'])
        self.log('val_map_75', map_metrics['map_75'])
        self.log('val_map_large', map_metrics['map_large'])
        self.log('val_map_medium', map_metrics['map_medium'])
        self.log('val_map_small', map_metrics['map_small'])
        print(f'Validation mAP: {map_metrics}')
        self.map_metric.reset()  # リセット

    def test_step(self, batch):
        x, t = batch
        outputs = self(x)
        self.map_metric.update(outputs, t)
        return outputs

    def on_test_epoch_end(self):
        # mAPの各値をログ
        map_metrics = self.map_metric.compute()
        self.log('test_map', map_metrics['map'])
        self.log('test_map_50', map_metrics['map_50'])
        self.log('test_map_75', map_metrics['map_75'])
        self.log('test_map_large', map_metrics['map_large'])
        self.log('test_map_medium', map_metrics['map_medium'])
        self.log('test_map_small', map_metrics['map_small'])
        print(f'Test mAP: {map_metrics}')
        self.map_metric.reset()


    def configure_optimizers(self):
        params = [p for p in self.ssd300.parameters() if p.requires_grad]
        optimizer = torch.optim.Adam(params)
        scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.5)
        return [optimizer], [scheduler]