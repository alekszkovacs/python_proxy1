# python_proxy1
Az ebben a repoban található mini python projekt tartalmaz egy klienst, egy proxy és egy "valódi" szervert, melyek websocketeken keresztül kommunikálnak egymással.
A [how_to_use.pdf](https://github.com/alekszkovacs/python_proxy1/files/8332273/how_to_use.pdf) dokumentumban megmutatotthoz hasonlóan el kell indítani először a szervert egy megadott ip-n és porton, majd ugyanezt megcsinálni a proxy szerverrel is, aminek meg kell adni ezen túl azt is, hogy a szerver melyik ip-n és porton érhető el, majd ezek után a klienst csatlakoztatni kell a proxy szerverre úgy, hogy megadunk neki egy json fájlt.
A program lényege az, hogy amennyiben a json fájl nem tartalmaz 20 karakternél hosszabb kifejezést, akkor a proxy szerver átengedi a kliens kérelmét, és a szerver generálni fog a json fájl tartalmából egy kliens által meghatározott típusú hash-t. Ha van a fájlban 20 karakternél hosszabb szó, akkor a proxy szerver megszűri a kérelmet és kiírja a TILOS kifejezést.

A program egy egyetemi ZH-ra beadott megoldásom. 
