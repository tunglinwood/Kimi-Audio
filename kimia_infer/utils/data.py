import torch


class KimiAContent:
    def __init__(
        self, audio_token_ids=None, text_token_ids=None, is_continuous_mask=None, audio_token_loss_mask=None, text_token_loss_mask=None
    ):
        self.audio_token_ids: list[int] = audio_token_ids or []
        self.text_token_ids: list[int] = text_token_ids or []
        self.is_continuous_mask: list[int] = is_continuous_mask or []

        self.audio_token_loss_mask: list[int] = audio_token_loss_mask or []
        self.text_token_loss_mask: list[int] = text_token_loss_mask or []

        self.continuous_feature = []

    def audio_append(self, index: int, is_continuous: bool = False, audio_token_loss_mask: bool = False):
        self.audio_token_ids.append(index)
        self.is_continuous_mask.append(is_continuous)
        self.audio_token_loss_mask.append(audio_token_loss_mask)

    def text_append(self, index: int, text_token_loss_mask: bool = False):
        self.text_token_ids.append(index)
        self.text_token_loss_mask.append(text_token_loss_mask)

    def audio_extend(self, ids: list[int], is_continuous: bool = False, audio_token_loss_mask: bool = False):
        self.audio_token_ids.extend(ids)
        self.is_continuous_mask.extend([is_continuous] * len(ids))
        self.audio_token_loss_mask.extend([audio_token_loss_mask] * len(ids))

    def text_extend(self, ids: list[int], text_token_loss_mask: bool = False):
        self.text_token_ids.extend(ids)
        self.text_token_loss_mask.extend([text_token_loss_mask] * len(ids))

    def audio_prepend(self, index: int, is_continuous: bool = False, audio_token_loss_mask: bool = False):
        self.audio_token_ids = [index] + self.audio_token_ids
        self.is_continuous_mask = [is_continuous] + self.is_continuous_mask
        self.audio_token_loss_mask = [audio_token_loss_mask] + self.audio_token_loss_mask

    def text_prepend(self, index: int, text_token_loss_mask: bool = False):
        self.text_token_ids = [index] + self.text_token_ids
        self.text_token_loss_mask = [text_token_loss_mask] + self.text_token_loss_mask

    def audio_pretend(self, ids: list[int], is_continuous: bool = False, audio_token_loss_mask: bool = False):
        self.audio_token_ids = ids + self.audio_token_ids
        self.is_continuous_mask = [is_continuous] * len(ids) + self.is_continuous_mask
        self.audio_token_loss_mask = [audio_token_loss_mask] * len(ids) + self.audio_token_loss_mask

    def text_pretend(self, ids: list[int], text_token_loss_mask: bool = False   ):
        self.text_token_ids = ids + self.text_token_ids
        self.text_token_loss_mask = [text_token_loss_mask] * len(ids) + self.text_token_loss_mask

    def merge(self, other: "KimiAContent"):
        self.audio_token_ids.extend(other.audio_token_ids)
        self.text_token_ids.extend(other.text_token_ids)
        self.is_continuous_mask.extend(other.is_continuous_mask)
        self.audio_token_loss_mask.extend(other.audio_token_loss_mask)
        self.text_token_loss_mask.extend(other.text_token_loss_mask)
        self.continuous_feature.extend(other.continuous_feature)

    def to_tensor(self) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        return (
            torch.tensor([self.audio_token_ids], dtype=torch.long),
            torch.tensor([self.text_token_ids], dtype=torch.long),
            torch.tensor([self.is_continuous_mask], dtype=torch.bool),
            torch.tensor([self.audio_token_loss_mask], dtype=torch.bool),
            torch.tensor([self.text_token_loss_mask], dtype=torch.bool),
        )

    def is_valid(self):
        return (
            len(self.audio_token_ids)
            == len(self.text_token_ids)
            == len(self.is_continuous_mask)
            == len(self.audio_token_loss_mask)
            == len(self.text_token_loss_mask)
        )
