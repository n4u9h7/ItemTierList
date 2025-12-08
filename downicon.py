<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>ARC Raiders Complete Loot Tier List</title>
    <style>
        body { background-color: #0d1117; color: #c9d1d9; font-family: 'Segoe UI', sans-serif; margin: 0; padding: 20px; }
        .header { text-align: center; padding: 30px; border-bottom: 1px solid #30363d; margin-bottom: 30px; }
        h1 { color: #58a6ff; }
        .container { max-width: 1200px; margin: 0 auto; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 15px; }
        .card { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 15px; text-align: center; }
        .card:hover { border-color: #58a6ff; transform: translateY(-3px); transition: 0.2s; }
        .img-box { width: 100px; height: 100px; margin: 0 auto 10px; display: flex; align-items: center; justify-content: center; background: #0d1117; border-radius: 5px; }
        .img-box img { max-width: 100%; max-height: 100%; object-fit: contain; }
        .name { font-size: 0.85rem; font-weight: bold; margin-bottom: 8px; height: 35px; overflow: hidden; display: flex; align-items: center; justify-content: center; }
        .price { color: #3fb950; font-weight: bold; font-size: 1.1rem; }
        .tier { font-size: 0.7rem; padding: 2px 5px; border-radius: 3px; margin-top: 5px; display: inline-block; }
        .S { background: #da3633; } .A { background: #d29922; } .B { background: #1f6feb; } .C { background: #6e7681; }
    </style>
</head>
<body>

<div class="header">
    <h1>ARC RAIDERS LOOT VALUE TIERS</h1>
    <p>전체 아이템 가격순 정렬 (로컬 이미지 버전)</p>
</div>

<div class="container">
    <div class="grid" id="mainGrid"></div>
</div>

<script>
    const allLoot = [
        { name: "Snap Hook", price: 14000, tier: "S" },
        { name: "Queen Reactor", price: 13000, tier: "S" },
        { name: "Matriarch Reactor", price: 13000, tier: "S" },
        { name: "Lance's Mixtape (5th Edition)", price: 10000, tier: "S" },
        { name: "Kinetic Converter", price: 7000, tier: "S" },
        { name: "Anvil Splitter", price: 7000, tier: "S" },
        { name: "Breathtaking Snow Globe", price: 7000, tier: "S" },
        { name: "Horizontal Grip", price: 7000, tier: "S" },
        { name: "Silencer III", price: 7000, tier: "S" },
        { name: "Ion Sputter", price: 6000, tier: "S" },
        { name: "Magnetron", price: 6000, tier: "S" },
        { name: "Magnetic Accelerator", price: 5500, tier: "S" },
        { name: "Power Rod", price: 5500, tier: "S" },
        { name: "Heavy Shield", price: 5500, tier: "S" },
        { name: "Explosive Mine Blueprint", price: 5000, tier: "S" },
        { name: "Leaper Pulse Unit", price: 5000, tier: "S" },
        { name: "Light Gun Parts Blueprint", price: 5000, tier: "S" },
        { name: "Red Coral Jewelry", price: 5000, tier: "S" },
        { name: "Playing Cards", price: 5000, tier: "S" },
        { name: "Energy Ammo Blueprint", price: 5000, tier: "S" },
        { name: "Spectrum Analyzer", price: 3500, tier: "A" },
        { name: "Geiger Counter", price: 3500, tier: "A" },
        { name: "Silver Teaspoon Set", price: 3000, tier: "A" },
        { name: "Statuette", price: 3000, tier: "A" },
        { name: "Flow Controller", price: 3000, tier: "A" },
        { name: "Microscope", price: 3000, tier: "A" },
        { name: "Fine Wristwatch", price: 3000, tier: "A" },
        { name: "Vita Spray", price: 2880, tier: "B" },
        { name: "Exodus Modules", price: 2750, tier: "B" },
        { name: "Bison Driver", price: 2500, tier: "B" },
        { name: "Showstopper", price: 2200, tier: "B" },
        { name: "Very Comfortable Pillow", price: 2000, tier: "B" },
        { name: "Turbo Pump", price: 2000, tier: "B" },
        { name: "Laboratory Reagents", price: 2000, tier: "B" },
        { name: "Snitch Scanner", price: 2000, tier: "B" },
        { name: "Cooling Fan", price: 2000, tier: "B" },
        { name: "Medium Shield", price: 2000, tier: "B" },
        { name: "Rocket Thruster", price: 2000, tier: "B" },
        { name: "Portable TV", price: 2000, tier: "B" },
        { name: "Advanced Electrical Components", price: 1750, tier: "B" },
        { name: "Mod Components", price: 1750, tier: "B" },
        { name: "Trailblazer Grenade", price: 1600, tier: "B" },
        { name: "Explosive Mine", price: 1500, tier: "B" },
        { name: "Surge Shield Recharger", price: 1200, tier: "B" },
        { name: "ARC Flex Rubber", price: 1000, tier: "C" },
        { name: "Broken Flashlight", price: 1000, tier: "C" },
        { name: "Torn Book", price: 1000, tier: "C" },
        { name: "Explosive Compound", price: 1000, tier: "C" },
        { name: "Remote Control", price: 1000, tier: "C" },
        { name: "Garlic Press", price: 1000, tier: "C" },
        { name: "Coffee Pot", price: 1000, tier: "C" },
        { name: "Zipline", price: 1000, tier: "C" },
        { name: "Antiseptic", price: 1000, tier: "C" },
        { name: "Smoke Grenade", price: 1000, tier: "C" },
        { name: "ARC Motion Core", price: 1000, tier: "C" },
        { name: "ARC Circuitry", price: 1000, tier: "C" },
        { name: "Industrial Battery", price: 1000, tier: "C" },
        { name: "Rubber Duck", price: 1000, tier: "C" },
        { name: "Fertilizer", price: 1000, tier: "C" },
        { name: "Agave", price: 1000, tier: "C" },
        { name: "Coolant", price: 1000, tier: "C" },
        { name: "Empty Wine Bottle", price: 1000, tier: "C" },
        { name: "Mushroom", price: 1000, tier: "C" },
        { name: "Jolt Mine", price: 850, tier: "C" },
        { name: "Shrapnel Grenade", price: 800, tier: "C" },
        { name: "Heavy Gun Parts", price: 700, tier: "C" },
        { name: "Mechanical Components", price: 640, tier: "C" }
    ];

    // 가격 높은 순 정렬 (이미 되어있지만 재확인)
    allLoot.sort((a, b) => b.price - a.price);

    const grid = document.getElementById('mainGrid');
    allLoot.forEach(item => {
        // 이미지 경로 처리 (파일명에서 불필요한 특수문자 제거)
        const safeName = item.name.replace(/[\\/:*?"<>|]/g, '');
        const imgSrc = `arc_loot_images/${safeName}.webp`;

        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = `
            <div class="img-box">
                <img src="${imgSrc}" onerror="this.src='https://via.placeholder.com/100?text=NONE';">
            </div>
            <div class="name">${item.name}</div>
            <div class="price">${item.price.toLocaleString()}</div>
            <div class="tier ${item.tier}">${item.tier} Tier</div>
        `;
        grid.appendChild(card);
    });
</script>
</body>
</html>