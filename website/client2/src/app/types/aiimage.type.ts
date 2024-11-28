import { PromptType } from "./prompt.type";

export class AiImageType {
    cfg_scale: number = 7;
    height: number = 512;
    width: number = 512;
    sampler: string = "K_DPM_2_ANCESTRAL";
    samples: number = 1;
    steps: number = 30;
    text_prompts: Array<PromptType> = [];
}