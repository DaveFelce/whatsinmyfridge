# whatsinmyfridge
Search for recipes for the ingredients scattered around your fridge and cupboards.

Enter some search terms and observe the beautiful graphs!  

Graph one shows the percentage match of your ingredients for the top 12 results.  Hover over the recipe names on the left to see which ingredients have matched and click anywhere on the filled in portion of the graphic to follow the link to the recipe.

Graphs two and three show the view of the search result data, in clockwise order of relevance - most 'interesting' first.  Again, click on the graphic for the recipe website link.  Relevance here is as determined by the Elasticsearch backend, which uses:

1. Word (term) frequency within the field - ingredients in this case
2. Inverse word frequency within all documents (you might have beef listed 12 times in a single field but if beef is a common word across all documents its relevance score is reduced)
3. Length of field: if your term matches two out of only three words in a field they score higher than if the field contains 20 separate words.
4. Proximity: how close are the keywords you chose together?  Not necessarily in the order you entered them.

