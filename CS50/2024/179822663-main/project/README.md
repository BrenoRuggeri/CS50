# BRENO'S BLOCKER
#### Video Demo:  <https://www.youtube.com/watch?v=VRTm4J7UvhU>
#### Description:
> Breno's Blocker is a Chrome extension designed to help users block unwanted ads on websites they visit, improving their browsing experience. By intercepting network requests, the extension stops ads from being loaded, making the web cleaner and faster.

**How it work ?**
> Essentially, my extension works by blocking network requests from websites that are responsible for displaying advertisements. By analyzing the URLs associated with these requests, the extension prevents the loading of ad content, ensuring users see only the content they want to view.

**Example**
> Imagine you're browsing YouTube and click on a video to watch. Your browser sends a request to YouTube, essentially saying, "Hey YouTube, I want to see this video." Once YouTube receives this request, it processes the video and sends the content back to you. However, along with the video content, YouTube also sends back additional requests from third-party advertisers, which are responsible for showing the ads you typically see during videos or on the sidebars of the site. These extra requests are what my extension blocks.

> By blocking these requests before they load on your browser, my extension prevents ads from ever reaching your screen, letting you enjoy content without interruptions.

**How my extension work ?**
> When you visit a website like YouTube with my extension enabled, the Chrome browser still makes the initial request to load the page. However, the extension intervenes and blocks additional requests to third-party advertisers.

> This process occurs seamlessly because the extension runs in the background alongside your browser. It listens for network requests made by the browser and filters out requests that match known patterns of ad networks. It ensures your browser doesn’t send requests to these ad servers, effectively stopping ads before they even get a chance to load.

**Manifest.json**
> The manifest.json file is the heart of every Chrome extension. It contains essential information about the extension, such as its name, version, description, permissions, and background processes. This file must follow a specific format defined by Chrome to ensure the extension functions correctly.

> To get started, I created a JSON object and populated it with the basic properties needed for the extension to function. Key properties included "name", "version", "description", "permissions", and "background". These properties define the basic identity of the extension and its functionality.

> Inside the "permissions" property, I listed all the Chrome APIs that my extension needs access to. For example, the WebRequest API allows the extension to monitor and block network requests, and the WebRequestBlocking API provides the ability to cancel requests.

> Additionally, inside the "background" property, I defined an object that includes a "scripts" property, which contains an array of scripts that run in the background. These scripts help manage the main logic of the extension.

  **Which Chrome APIs we need permition ?**
  > The extension uses several Chrome APIs that require explicit permission. These permissions are necessary for the extension to function properly:

  1. WebRequest: This API allows the extension to intercept network requests made by the browser. It is essential for analyzing all requests, including those made for ads.

  2. WebRequestBlocking: This is a companion API to WebRequest, allowing the extension to block or cancel requests. It is used to prevent ads from loading by blocking requests to ad servers.

  3. Special Permission for all_urls: This permission is required to ensure that the WebRequest and WebRequestBlocking APIs can be applied to all URLs, including those on every website the user visits. Without this permission, the extension would be limited to blocking ads only on certain websites.

**Icons**
> The "icons" property in the manifest.json file is crucial for user experience. It defines the icons that represent the extension in the browser toolbar, making it easy for users to identify and access the extension quickly.

> Icons also serve an additional purpose: they ensure that the extension complies with Chrome’s design guidelines, giving the extension a clear visual presentation. These icons are usually defined in various sizes, such as 16x16, 48x48, and 128x128, to ensure they display correctly across different areas of the browser interface.

> For this extension, I created a set of icons in these sizes and stored them in a file called "icons". This helps users visually identify the extension and easily toggle its features.

**Property Manifest Json**
> The "manifest_version" property defines the version of the manifest format that the extension uses. In this case, I used version 2.

**Background.js**
> The background.js file is a key part of the extension. It’s a background service script that remains active and manages the core logic of the extension, even when the browser is in the background.

> This file is responsible for processing and applying block lists, which define the domains and URLs of the websites that should be blocked. It monitors requests made by the browser and blocks those that match entries in the block lists. The background.js script ensures that ads are blocked in real time by continuously analyzing network requests.

**Chrome.webRequest.onBeforeRequest.addListener()**
> One of the most important methods used in the extension is chrome.webRequest.onBeforeRequest.addListener(). This method allows the extension to intercept network requests made by the browser before they are sent. This interception is key to blocking ads.

> The addListener method accepts three arguments. The first argument is a callback function that processes the request details. This function receives information about the request, such as the URL, type of request, and more. By analyzing this data, the extension can decide whether to block the request or not.

> The callback can be used to block requests. In fact, at this point, every request that matches certain criteria (like ad-related domains) will be blocked. To achieve this, I created an object that defines the filter criteria—essentially a list of URLs that the callback will apply to. Inside this object, I added a property called urls, which is an array. This array contains all the URLs of the sites from which ads should be blocked.

> After setting up this filter, I used a constant called defaultFilters and included all the URLs I want to block inside it.
