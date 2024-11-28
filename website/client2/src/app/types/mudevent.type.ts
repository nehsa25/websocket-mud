import { MudEvents } from "./mudevents.type";

export class MudEvent {
    type: MudEvents = MudEvents.NONE;
    message: string = "";
    name: string = "";
    description: string = "";
    people: string = "";
    monsters: Monster[] = [];
    items: string = "";
    exits: string = "";
    value: string = "";
    extra: string = "";
    map_contents: string = "";
    room_image_name: string = "";
    image_name: string = "";
    map_image_name: string = "";
    players: string = "";
    num_players: number = -1;
    is_resting: boolean = false;
    is_posioned: boolean = false;
    world_name: string = "";
    help_commands: HelpEvent = new HelpEvent();
    inventory: InventoryEvent = new InventoryEvent();
    npcs: string = "";
    statuses: any = {};
}

export enum MonsterAlignment {
    GOOD = 0,
    NEUTRAL = 1,
    EVIL = 2
}

export class Monster {
    name: string = "";    
    alignment: MonsterAlignment = MonsterAlignment.NEUTRAL;
}

export class InventoryEvent {
    items = new Array<any>();
    money = 0;
}

export class HelpEvent {
    commands = new Array<any>();
}

export class HelpCommand {
    command: string = "";
    description: string = "";
}