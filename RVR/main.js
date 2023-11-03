var Color = 0;


var _colors = [{"r":0,"g":133,"b":104},{"r":0,"g":147,"b":179},{"r":255,"g":224,"b":54},{"r":246,"g":31,"b":46}];

async function startProgram() {
    listenForColorSensor(_colors);

    setMainLed({ r: 255, g: 123, b: 13 });
    resetAim();
    setHeading(0);
    setSpeed(50);
}

async function onColor(color) {
    if (color.r !== 0 || color.g !== 133 || color.b !== 104) return;

    setMainLed({ r: 1, g: 255, b: 92 });
    setHeading(0);
    setSpeed(50);
}
registerEvent(EventType.onColor, onColor);

async function onColor_2(color) {
    if (color.r !== 0 || color.g !== 147 || color.b !== 179) return;

    setMainLed({ r: 4, g: 22, b: 255 });
    await roll(180, 10, 0);
    setHeading(180);
    setSpeed(50);
}
registerEvent(EventType.onColor, onColor_2);

async function onColor_3(color) {
    if (color.r !== 255 || color.g !== 224 || color.b !== 54) return;

    setMainLed({ r: 255, g: 241, b: 56 });
    setSpeed(145);
    await delay(0.5);
    stopRoll();
    await roll(90, 10, 0);
    setHeading(90);
    setSpeed(50);
}
registerEvent(EventType.onColor, onColor_3);

async function onColor_4(color) {
    if (color.r !== 246 || color.g !== 31 || color.b !== 46) return;

    setMainLed({ r: 255, g: 8, b: 8 });
    await roll(270, 10, 0);
    setHeading(270);
    setSpeed(50);
}
registerEvent(EventType.onColor, onColor_4);