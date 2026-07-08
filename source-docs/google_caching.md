The [Interactions API](</gemini-api/docs/interactions-overview>) is now generally available. We recommend using this API for access to all the latest features and models. 

  * [ Home ](<https://ai.google.dev/>)
  * [ Gemini API ](<https://ai.google.dev/gemini-api>)
  * [ Docs ](<https://ai.google.dev/gemini-api/docs>)

#  Context caching

In a typical AI workflow, you might pass the same input tokens over and over to a model. The Gemini API offers implicit caching to optimize performance and costs.

**Note:** This version of the page covers the **Interactions API** , which only supports implicit caching. Explicit caching \(manually creating and managing cache objects\) is not supported in the Interactions API. You can use the toggle on this page to switch to the [generateContent API version of this page](</gemini-api/docs/generate-content/caching>).

## Implicit caching

Implicit caching is enabled by default for all Gemini 2.5 and newer models. We automatically pass on cost savings if your request hits caches. There is nothing you need to do in order to enable this. The minimum input token count for context caching is listed in the following table for each model:

Model | Min token limit  
---|---  
Gemini 3.5 Flash | 4096  
Gemini 3.1 Pro Preview | 4096  
Gemini 2.5 Flash | 2048  
Gemini 2.5 Pro | 2048  
  
To increase the chance of an implicit cache hit:

  * Try putting large and common contents at the beginning of your prompt
  * Try to send requests with similar prefix in a short amount of time

You can see the number of tokens which were cache hits in the response object's `usage_metadata` \(Python\) or `usageMetadata` \(JavaScript\) field.