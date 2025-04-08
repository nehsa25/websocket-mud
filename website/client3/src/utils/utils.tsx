const medievalNames = [
    "Aelric", "Aldred", "Alaric", "Baldwin", "Bartholomew", "Beorn", "Cedric", "Dunstan",
    "Eamon", "Edmund", "Einar", "Elric", "Finnian", "Godric", "Grimbald", "Hadrian",
    "Havelock", "Hereward", "Ivo", "Jocelyn", "Kenelm", "Leif", "Llewellyn", "Magnus",
    "Marmaduke", "Neville", "Odo", "Osric", "Percival", "Quentin", "Ranulf", "Reginald",
    "Roderick", "Roland", "Sigurd", "Snorri", "Thane", "Theodoric", "Torin", "Ulric",
    "Valerian", "Viggo", "Waldemar", "Wayland", "Wulfric", "Ygraine", "Zephyrin",
    "Aethelred", "Cador", "Elowen", "Finnguala", "Gawain", "Isolde", "Kenric", "Lyra",
    "Oberon", "Rowena", "Tristan", "Guinevere", "Merlin", "Arthur", "Mordred", "Lancelot",
    "Gareth", "Bedivere", "Kay", "Yvain", "Erec", "Geraint", "Percivale"
];

export const getUsername = (): string => {
    const randomIndex = Math.floor(Math.random() * medievalNames.length);
    return medievalNames[randomIndex];
};