DEMO_CASES = [
{
"title":"The Midnight Gallery Theft","difficulty":"Standard",
"intro":"At 11:40 PM, the rare Star of Veyra diamond vanished from a locked gallery. The alarm was briefly disabled, but there was no sign of forced entry.",
"location":"Veyra City Museum — East Gallery",
"incident":"The diamond disappeared during a seven-minute power fluctuation. Three people had access to the gallery corridor.",
"suspects":[
{"name":"Mara Voss","role":"Museum Curator","motive":"Her department faced budget cuts and she knew the display schedule.","alibi":"Claims she was cataloguing paintings in the west wing.","statement":"I never went near the east gallery after the evening tour."},
{"name":"Elias Trent","role":"Night Guard","motive":"Recently acquired significant gambling debts.","alibi":"Says he was checking the loading entrance at 11:35 PM.","statement":"The camera outage was caused by the storm. I reported it immediately."},
{"name":"Nina Vale","role":"Restoration Specialist","motive":"Believed the museum had hidden the diamond's disputed ownership history.","alibi":"Says she was in the restoration lab mixing varnish.","statement":"I left my tools in the lab. I did not touch the display."}],
"evidence":[
{"name":"Dry Umbrella","description":"A folded umbrella near the east corridor. Its fabric is completely dry despite heavy rain outside."},
{"name":"Security Log","description":"The alarm was disabled using a curator-level access card at 11:36 PM."},
{"name":"Blue Pigment","description":"A tiny fleck of restoration pigment was found on the display latch."},
{"name":"Gallery Dust","description":"A clean rectangular patch in the dust suggests a flat object was placed beside the display."}],
"puzzle":{"title":"Reconstruct the Timeline","description":"The alarm was disabled at 11:36. The guard's loading-door scan was recorded at 11:38. The diamond was last seen at 11:34. How many minutes passed between the last confirmed sighting and alarm disablement? Enter a number.","answer":"2"},
"hints":["Compare the evidence with each suspect's access and work area.","The access card and pigment are more useful than the weather.","The curator-level card points toward Mara; the pigment is a planted distraction from restoration work."],
"solution":{"culprit":"Mara Voss","explanation":"The curator-level card disabled the alarm at 11:36, only two minutes after the diamond was last seen. Mara had curator access and falsely claimed she never approached the east gallery. The dry umbrella was a deliberate attempt to suggest someone entered from outside."}
},
{
"title":"Whispers at Blackthorn Manor","difficulty":"Easy",
"intro":"A priceless handwritten letter vanished from a study during a family gathering. The study door was locked, and everyone insists they stayed in the dining room.",
"location":"Blackthorn Manor — Private Study",
"incident":"The letter was present at 8:00 PM and missing by 8:20 PM. A small trail of candle wax leads toward the bookcase.",
"suspects":[
{"name":"Victor Blackthorn","role":"Estate Owner","motive":"The letter could reveal an embarrassing family secret.","alibi":"Says he remained at the dinner table.","statement":"No one in this family would steal from me."},
{"name":"Clara Wren","role":"Family Archivist","motive":"Wanted to protect the letter from being sold.","alibi":"Claims she was arranging books in the library.","statement":"I have never seen the hidden compartment."},
{"name":"Jonas Reed","role":"House Manager","motive":"Was promised a bonus if the letter was found before auction.","alibi":"Says he was lighting candles in the hallway.","statement":"I only entered the study earlier that afternoon."}],
"evidence":[
{"name":"Wax Drip","description":"Fresh candle wax is present beside the bookcase."},
{"name":"Loose Book","description":"One book sits slightly forward, hiding a narrow compartment."},
{"name":"Glove Fibre","description":"A dark wool fibre is caught on the compartment edge."}],
"puzzle":{"title":"The Hidden Compartment","description":"A shelf has 5 books. The hidden compartment is behind the middle book. Which numbered book is it, counting from the left?","answer":"3"},
"hints":["Look for the physical route to the hidden compartment.","The wax trail indicates someone used the hallway candle.","The middle of five books is book number 3; Jonas was lighting candles."],
"solution":{"culprit":"Jonas Reed","explanation":"The fresh wax trail leads to the bookcase, and Jonas was the person lighting candles in the hallway. He had a reason to enter the study and knew the house layout."}
}
]
