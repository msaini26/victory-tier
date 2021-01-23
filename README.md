# victory-tier

## Inspiration
An exceedingly hectic fantasy basketball draft and a desire to demonstrate how classical ML/NLP algorithms can sometimes be superior were strong motivations. 

## What it does
Simply type in the name of your favorite NBA player and we’ll get you all of their stats. Using our robust pattern matching algorithms, we can find any player you look for, no matter how many typos you add. In addition, we'll give you three new players who play similarly to your queried player. 

## How we built it
Here's how it works:
1. Your query goes through an ensemble of fuzzy string matching algorithms to get the closest-matching player. Some filters specialize in partial substrings, for individual first and last names, while others look at edit distance. 
2. Now that we’ve found the player you’re looking for, we have to find his three closest players. We do this by associating each player with a set of preprocessed normalized features. We can then sort by euclidean distance to get an efficient matching. The interesting thing is that we don’t take a player’s position into account at all, yet players of similar positions tend to cluster together. 
3. Finally, we send all four calculated players back to the frontend, where a bit of javascript and css magic makes everything come together! 

## Challenges we ran into
Our biggest challenge dealt with the integration of our frontend and backend codebases. Designing a clean API and debugging various network bugs turned out to be very tedious. 

## Accomplishments that we're proud of
Our clean, user interface with its gradient color scheme and pretty fonts is definitely something to be proud of. Getting it to work well in many contexts (browsers, aspect ratios) took a lot of learning-on-the-fly and teamwork. 

The backend ML algorithms worked surprisingly well, too. After applying normalization and PCA, the dataset had a really nice structure. Our model did not take playing position into account as one of its features, yet players of the same position tend to be clustered together. Also, the pattern matching for the search was surprisingly robust. 

## What we learned
While developing Victory Tier, Mansi learned the backend development functions through mentorship by her older brother, Rajan. This was our first time working together on a hackathon project. We learned to be adaptable and the importance of communication throughout. 

## What's next for Victory Tier
We hope to improve our user interface and responsiveness on our website. We hope to take our web application and create a mobile application for fanatics on-the-go.
