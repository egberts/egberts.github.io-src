Title: Firefox Sync
Date: 2017-05-20T16:59
Modified: 2025-07-13T05:09
Tags: Firefox, sync
Category: research
Summary: Firefox Sync is a built-in web browser add-in application and an application network protocol.
Status: published

Firefox Sync can synchronize between your own Firefox web browsers over
different devices for the following:

* Bookmarks
* Opened tabs
* Passwords
* History of browsed web pages
* Add-Ons (not available on iOS mobile devices)
* Preferences (not available on iOS mobile devices)

Application Program
*******************

Setup by GUI
============

Setup by command line
---------------------

On the UNIX platform, Firefox stores its preference data settings in the `$HOME/.mozilla/firefox` directory. Check for your specific profile subdirectory in the `$HOME/.mozilla/firefox/profiles.ini` file.

Add the following lines to the `user.js` file.

Notice: Any and all changes toward ``preferences.js`` will be blown` away by the next Firefox upgrade.

[jtable]
Column, Description
"`prefs.js:user_pref(\"services.sync.username\", johndoe@example.com")`", The Sync account name (maintained by Firefox Account Manager)
"`prefs.js:user_pref(\"services.sync.declinedEngines\", \"tabs,addons,passwords,history\");`", A list of things to keep track of. Valid options are tabs, addons, passwords, history.
"`prefs.js:user_pref(\"services.sync.account\", \"johndoe@example.com\");`", client
account name used on Firefox sync, typically in email format.
`prefs.js:user_pref("services.sync.client.name", "johndoe' Firefox on johndoe-macbook");`, client account label used on Firefox Sync, a simple representation
[/jtable]

Firefox Sync Network Protocol
=============================

To set up a private Firefox sync server.

Firefox Sync Server
-------------------

To host a private server of Firefox Sync, see [https://mozilla-services.readthedocs.io/en/latest/howtos/run-sync-1.5.html%7CHowTo](https://mozilla-services.readthedocs.io/en/latest/sync/index.html)

Downsides
----

Only problem is that there is ZERO configurable setting in iOS nor Android app to set this to your own private server of Firefox Sync.

Dead ... on ... arrival, this protocol is.

Misdirection on iOS
====
On the Firefox iOS app, you cannot directly change or set a custom Firefox Sync server through the app’s interface. The option to customize the Firefox Sync server is available on desktop versions of Firefox (macOS, Windows, Linux), but not on the iOS version.

However, you can still achieve this indirectly by syncing Firefox on your desktop with your custom sync server first, and then syncing your iOS device with that same account. Here’s how to do it:

### 1. **Set up Firefox Sync on Desktop with a Custom Server**

* On your desktop, open Firefox and go to **Settings**.
* Scroll down to **Firefox Account** and sign in (or create an account if you don’t have one).
* In the **about\:config** page (type `about:config` in the address bar), search for `services.sync` and modify the server URL to point to your custom Sync server.

Example:

* `identity.fxaccounts.remote.uri` (for signing in)
* `services.sync.serverURL` (for syncing data)

**Note**: You’ll need your own custom Firefox Sync server set up for this step. There are guides online for setting up your own Sync server if needed.

### 2. **Sync Your iOS Device**

* Once your desktop is set up with the custom server and syncing properly, open the Firefox app on your iOS device.
* Log in with the same Firefox account you used on your desktop.
* Firefox will sync the data between your desktop and iOS, including bookmarks, history, and open tabs.

### 3. **Managing Sync (iOS)**

You won’t be able to change the Sync server directly from the iOS app, but your device will sync to the server associated with your Firefox account as long as you’ve set it up on your desktop beforehand.


Internals
====

To dive into the **internals** of the **Firefox Sync Server Protocol** and its use in the **iOS Firefox app**, let's break down the core components involved, especially regarding how Firefox syncs data and the underlying protocols that are utilized.

### 1. **Overview of Firefox Sync Architecture**

Firefox Sync is a cloud-based synchronization service provided by Mozilla that keeps users’ data (bookmarks, passwords, history, tabs, etc.) synchronized across devices. The protocol has several components that interact to perform this synchronization. The iOS app, like other Firefox clients, communicates with a **Sync server** that handles user data.

The core parts involved in Firefox Sync are:

* **Firefox Sync Client** (iOS, Android, Desktop)
* **Firefox Sync Server** (the backend service handling data synchronization)
* **Sync Storage (on the server)**

When you install Firefox on a new device and sign in with your Firefox account, that device will start syncing with the backend Sync server to pull down your data. In the case of **iOS**, it’s the same protocol, but there are some differences due to the constraints and platform-specific factors on iOS.

---

### 2. **Sync Server Protocol Internals**

#### **2.1 The Sync Server Protocol (JSON-based)**

The Sync server protocol used by Firefox is primarily based on **JSON**. Here are the key aspects of the protocol:

* **Authentication & OAuth**:

  * When a client (like the iOS app) needs to authenticate with the Sync server, it uses **OAuth** tokens to verify the identity. The **OAuth2** flow is used, where the client (iOS app) requests permission to access the user's Firefox account. Once authenticated, an access token is generated.

* **RESTful Endpoints**:

  * Firefox Sync uses RESTful HTTP endpoints for data exchange between the client and the server. These endpoints deal with various types of data like bookmarks, passwords, history, etc.

    **Example endpoints**:

    * `/1.1/sync/1.5/:client_id/storage` - Syncs the storage data for the client.
    * `/1.1/sync/1.5/:client_id/collections` - Manages different collections (e.g., bookmarks, passwords).
    * `/1.1/sync/1.5/:client_id/login` - Authenticates the user or verifies credentials.

* **Data Format**:

  * The data sent between the client and server is typically in **JSON format**. This includes information like bookmarks, history, passwords, and metadata.

    Example of a simple sync payload for bookmarks:

    ```json
    {
      "items": [
        {
          "id": "abc123",
          "type": "bookmark",
          "title": "Mozilla",
          "url": "https://www.mozilla.org",
          "dateAdded": 1620132465000
        }
      ]
    }
    ```

#### **2.2 Storage and Syncing Flow**

Here’s how data flows between the client and the Sync server:

1. **Initial Authentication**: When you first open the Firefox app on your iOS device and log in, the app requests an OAuth token from the Sync server to authenticate the user.

2. **Syncing Data**: Once authenticated, the iOS app can start syncing data, which is done using a series of **POST**, **GET**, and **DELETE** requests over HTTP to the Sync server. For instance:

   * The iOS client can **GET** the data (bookmarks, history, etc.) from the Sync server.
   * It can also **POST** updates (new bookmarks, tabs, etc.) to the server.
   * The server will handle the conflict resolution and ensure that data is consistent across multiple devices.

3. **Storing Data on the Server**: Data is stored on the Sync server as a set of collections (bookmarks, history, tabs, etc.). These are essentially buckets where the data for each category is stored.

   Example:

   * Bookmarks and history are stored in **collections** like `bookmarks`, `history`, etc., on the server.
   * The server uses **client IDs** to manage which data belongs to which device.

#### **2.3 Sync Client on iOS**

On iOS, the Firefox Sync client is responsible for initiating sync operations, sending and receiving data, and ensuring that the data is consistent between the client and the server. The client operates in the following way:

* **Periodically Syncs Data**: Sync is performed periodically in the background (if allowed by iOS). The app syncs every time it is opened or after certain intervals.
* **Minimal API Usage**: Due to iOS limitations, the iOS app doesn’t have as much flexibility in managing sync as the desktop version. For example, background syncing and data transfer can be throttled or limited based on iOS's background task policies.

#### **2.4 Encryption**

The data transmitted between the client (iOS) and the Sync server is **end-to-end encrypted**. This means that the data is encrypted before it leaves the device, and only the device with the correct credentials can decrypt it.

* **Encryption key**: A master encryption key is used to encrypt and decrypt the data. This key is never sent to the Sync server and is only available on the client (your device).

---

### 3. **Changing Sync Server on iOS**

While you cannot directly modify the sync server on iOS, on the desktop version of Firefox (via `about:config`), there are preferences like `services.sync.serverURL` that allow you to point Firefox to a custom server. However, the iOS app will always sync with the default Mozilla Sync server unless Mozilla allows for custom server support in future versions.

For **custom Sync server configurations**, you'd typically modify your Firefox client to communicate with an internal server by setting it up with the `about:config` preferences. For iOS, this would still be limited by the default Firefox iOS app, and unless there’s direct support for custom servers, the sync will happen through Mozilla’s Sync infrastructure.

---

### 4. **Custom Sync Server**

If you decide to host your own custom sync server, Mozilla provides some resources and documentation on how to do this. A **custom Sync server** would typically include:

* **Mozilla's Sync Server Code**: An open-source project that you can run on your own servers.
* **Configuration of server**: Configuring server settings like authentication and data storage.

You can find this repository here:

* [Mozilla Sync Server GitHub](https://github.com/mozilla-services/syncserver)

---

### 5. **Potential Limitations on iOS**

While Firefox Sync works seamlessly across platforms, the iOS version is somewhat restricted by Apple’s app sandboxing and background task policies. For example:

* **Background syncing limitations**: iOS has strict policies on background tasks, which can lead to limitations on how often and when Firefox on iOS syncs in the background.
* **Custom Sync Server Support**: As of now, Firefox on iOS does not support easily changing or customizing the sync server URL.

---

### Conclusion

To summarize, while the **Firefox Sync Protocol** relies on **OAuth**, **REST APIs**, and **JSON data**, with **end-to-end encryption**, the iOS app itself does not allow for direct customization of the Sync server URL or settings. You’d need to set up your custom Sync server on the desktop version of Firefox, and iOS would sync with that server through the standard Sync API, provided that you authenticate with the same Firefox account.


iOS settings
====
On **Firefox iOS**, the settings related to **Firefox Sync** (such as the sync server configuration) are not as exposed as they are in the desktop version of Firefox. In fact, **Firefox for iOS** does **not allow for custom sync server configurations** directly from the app, unlike the desktop version, where you can modify server URLs in `about:config`.

That being said, the **Firefox Sync settings** on iOS are **largely controlled by the server URL and account information on Mozilla's side** and aren't stored or configurable in a way that is user-accessible.

### Here’s what you need to know:

1. **Sync Settings on Firefox for iOS**:

   * When you use the Firefox app on iOS, all your sync settings (including the sync server and your Firefox Account) are **stored in the app's internal settings** and managed via the Mozilla servers.
   * **Account Info**: The app stores your **Firefox Account** credentials (username and OAuth token) which allows you to sync data between devices. However, you can't directly change the sync server from within the app.

2. **Where Are These Settings Stored?**

   * On iOS, **app settings and preferences** like sync data, account credentials, and synchronization states are stored in the **app’s sandboxed storage**. Apple’s strict privacy and security measures do not allow easy access to these files from the outside.
   * **Keychain**: Account information (like the OAuth token used for Firefox Sync) is likely stored securely in the **iOS Keychain** — Apple’s encrypted storage system for sensitive data (like passwords, tokens, and certificates). However, this is not directly accessible unless you're familiar with tools for iOS app development or reverse-engineering.
   * **App Preferences**: Other basic app settings are stored in **UserDefaults**, which is a simple local storage mechanism in iOS, though sensitive information (like your Sync credentials) would be encrypted before storage.

3. **Limitations**:

   * The iOS app **does not allow for manual configuration of the Sync server URL** (for example, to point to a custom Sync server). This means you are restricted to the default Mozilla Sync infrastructure, and there’s no built-in option for changing the Sync server URL in the app.
   * On **desktop Firefox**, you can change the server via `about:config`, but there’s no equivalent mechanism on the iOS app.

4. **Syncing Behavior**:

   * When you log into Firefox on your iOS device, the app communicates with Mozilla’s Sync servers to fetch and upload your browsing data (like bookmarks, history, and open tabs).
   * The sync process uses the **OAuth token** for authentication and encryption, so only authorized clients can access your synced data.
   * The **sync server URL** for Mozilla’s infrastructure is embedded in the app itself and is not user-configurable.

### How Firefox Sync Works on iOS:

* **Initial Setup**: When you log into the Firefox app for the first time with your Firefox Account, it starts using Mozilla’s Sync servers by default. The sync data is stored in Mozilla's cloud, and your device fetches data through the standard sync endpoints.

* **Server Interaction**:

  * **Sync Server URL**: The URL for Mozilla’s Sync server is hardcoded into the app. This URL handles all communication between the client and server.
  * **Sync Data (bookmarks, history, tabs)**: The app retrieves and uploads data like bookmarks and browsing history to Mozilla’s server automatically, without any option to configure or redirect to a different server.

### Conclusion:

The **Firefox Sync Server settings** are stored internally within the app’s sandboxed storage and managed by **Mozilla's infrastructure**. They are not user-modifiable on iOS. If you’re looking to use a custom server for Firefox Sync, that can only be configured on desktop versions of Firefox (via `about:config`), not on the iOS app.

Unfortunately, the iOS version doesn’t provide any easy way to change or access these internal settings.

Hence, Mozilla corporation would be able to have the details of your private Firefox Sync Server: K, no thanks.
