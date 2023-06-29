# dominionWhitelistData
a statistical analysis of whitelist tickets on dominion minecraft server

here's the write-up, also at https://rentry.org/dominionWhitelistData

# Dominion Whitelist Analysis

So, since we've received multiple questions about whitelist acceptance rate and the like and my summer holidays have begun, I've spent some time over the last three days collecting and processing data on our whitelist tickets. The snapshot I took is from June 27th, so we'll be looking at data from the start of our ticket system on July 11, 2020 until June 27th, 2023. To begin, here's how the raw data looks:

-> ![raw data](https://media.discordapp.net/attachments/738839493183799318/1124080499732791347/Screenshot_2023-06-29_223947.png) <-

As you can see, I collected the **start** date of a ticket (not end); whether the ticket was accepted, denied, or the user left before a decision; the users which interacted with that ticket; their User IDs (to avoid having to deal with name changes); the link to the ticket; its number; and whether Legundo was mentioned. A ticket counts as accepted if the server IP is mentioned in it, denied if the phrase "wish you the best" is mentioned (from the deny copypasta), and withdrawn if neither are.

Let's start with some general stats. In this time, Dominion received 2939 applications. My script processed 2914 of them, so ~99.15%. Of these, we accepted 1313, so ~45.08%. Here are some graphs on the weekly total applications, accepted applications, and acceptance rates (the red lines are six-week moving averages):

-> ![weekly total applications](https://media.discordapp.net/attachments/738839493183799318/1124080500047355934/Total_Applications_per_Week.png) <-

-> ![weekly accepted applications](https://media.discordapp.net/attachments/738839493183799318/1124080499321741312/Accepted_Applications_per_Week.png) <-

-> ![weekly acceptance rate](https://media.discordapp.net/attachments/738839493183799318/1124080500315803658/Weekly_Acceptance_Rate.png) <-

Annually, the acceptance rates were 41.87%, 37.80%, 54.45%, 50.25% for 2020, 2021, 2022, and 2023 respectively. You can see in the graphs that the acceptance rate early on is really low. This is because admins would DM the user the server IP, so the script doesn't catch it as accepted. It only happened for the first few tickets though, so I'm fine with it being in there.

I'm sure you're wondering which of our lovely staff members have been the most industrious in processing tickets. Good thing we have data on that! Do be aware that interacting with a ticket counts every user who sent a message in it or interacted with the bot in it, so it will count even if you just close a completed ticket. Nevertheless, we can tell somewhat clearly that the top three are 🥇@bobthesnob (yay), 🥈@wilven, and🥉@astrogirl. Here's the full list:

-> ![tickets per staff member](https://media.discordapp.net/attachments/738839493183799318/1124083832937783426/Whitelist_Applications_Processed_per_Staff_Member.png) <-

Now, you might say that this is unfair because all the top ones have been around forever and our newer staff members haven't had time to catch up yet. Fear not, I've compiled this annually, monthly, and weekly too:

-> ![yearly tickets per staff member](https://media.discordapp.net/attachments/738839493183799318/1124083831989878896/Yearly_Whitelist_Applications_Processed_per_Staff_Member.png) <-

-> ![monthly tickets per staff member](https://media.discordapp.net/attachments/738839493183799318/1124083832631607397/Monthly_Whitelist_Applications_Processed_per_Staff_Member.png) <-

-> ![weekly tickets per staff member](https://media.discordapp.net/attachments/738839493183799318/1124083832333815959/Weekly_Whitelist_Applications_Processed_per_Staff_Member.png) <-

To end on some levity, here's the amount of times Legundo was mentioned in our whitelist tickets per month (only the months where it happened). Interestingly, the graph bears a passing resemblance to the google search interest of `dominion minecraft`:

-> ![legundo mentions](https://media.discordapp.net/attachments/738839493183799318/1124083831713058928/Legundo_Mentions_in_Whitelist_Tickets.png) <-

-> !["dominion minecraft" search interest](https://media.discordapp.net/attachments/738839493183799318/1124085874540413008/Screenshot_2023-06-29_231541.png) <-

That's it for today! You can look at the raw data at https://tinyurl.com/DominionWhitelistData, and look at the full code and snapshot I extracted data from at https://github.com/BobTheSnob1/dominionWhitelistData.
