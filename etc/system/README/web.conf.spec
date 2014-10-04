#   Version 6.0
#
# This file contains possible attributes and values you can use to configure Splunk's web interface.
#
# There is a web.conf in $SPLUNK_HOME/etc/system/default/.  To set custom configurations, 
# place a web.conf in $SPLUNK_HOME/etc/system/local/.  For examples, see web.conf.example.
# You must restart Splunk to enable configurations.
#
# To learn more about configuration files (including precedence) please see the documentation 
# located at http://docs.splunk.com/Documentation/Splunk/latest/Admin/Aboutconfigurationfiles


[settings]
	* Set general SplunkWeb configuration options under this stanza name.
	* Follow this stanza name with any number of the following attribute/value pairs.  
	* If you do not specify an entry for each attribute, Splunk will use the default value.

startwebserver = [0 | 1]
   	* Set whether or not to start SplunkWeb.
   	* 0 disables SplunkWeb, 1 enables it.
   	* Defaults to 1.

httpport = <port_number>
   	* Must be present for SplunkWeb to start.
   	* If omitted or 0 the server will NOT start an http listener.
        * If using SSL, set to the HTTPS port number.
   	* Defaults to 8000.

mgmtHostPort = <IP:port>
   	* Location of splunkd.
   	* Don't include http[s]:// -- just the IP address.
   	* Defaults to 127.0.0.1:8089.

splunkdConnectionTimeout = <integer>
    * Number of seconds to wait before timing out when communicating with splunkd
    * Must be at least 30
    * Values smaller than 30 will be ignored, resulting in the use of the default value
    * Defaults to 30

enableSplunkWebSSL = [True | False]
	* Toggle between http or https.
	* Set to true to enable https and SSL.
	* Defaults to False.
   
privKeyPath = etc/auth/splunkweb/privkey.pem
    * The path to the file containing the web server's SSL certificate's private key
    * Relative paths are interpreted as relative to $SPLUNK_HOME
       * Relative paths may not refer outside of $SPLUNK_HOME (eg. no ../somewhere)
    * An absolute path can also be specified to an external key
    * See also enableSplunkWebSSL and caCertPath

caCertPath = etc/auth/splunkweb/cert.pem
   * The path to the file containing the SSL certificate for the splunk web server
   * The file may also contain root and intermediate certificates, if required
     They should be listed sequentially in the order:
     [ Server's SSL certificate ]
     [ One or more intermediate certificates, if required ]
     [ Root certificate, if required ]
   * Relative paths are interpreted as relative to $SPLUNK_HOME
       * Relative paths may not refer outside of $SPLUNK_HOME (eg. no ../somewhere)
   * An absolute path can also be specified to an external certificate
   * See also enableSplunkWebSSL and privKeyPath

serviceFormPostURL = http://docs.splunk.com/Documentation/Splunk
   * This attribute is deprecated since 5.0.3

userRegistrationURL = https://www.splunk.com/page/sign_up
updateCheckerBaseURL = http://quickdraw.Splunk.com/js/
docsCheckerBaseURL = http://quickdraw.splunk.com/help
   * These are various Splunk.com urls that are configurable. 
   * Setting updateCheckerBaseURL to 0 will stop the SplunkWeb from pinging Splunk.com 
	 for new versions of itself. 

enable_insecure_login = [True | False]
   * Indicates if the GET-based /account/insecurelogin endpoint is enabled
   * Provides an alternate GET-based authentication mechanism
   * If True, the /account/insecurelogin?username=USERNAME&password=PASSWD is available
   * If False, only the main /account/login endpoint is available
   * Defaults to False

login_content = <content_string>
   * Add custom content to the login page
   * Supports any text including html 
   
supportSSLV3Only = [True | False]
   * Allow only SSLv3 connections if true
   * NOTE: Enabling this may cause some browsers problems

cipherSuite = <cipher suite string>
   * If set, uses the specified cipher string for the HTTP server.
   * If not set, uses the default cipher string
     provided by OpenSSL.  This is used to ensure that the server does not 
     accept connections using weak encryption protocols.
   
root_endpoint = <URI_prefix_string>
   * defines the root URI path on which the appserver will listen
   * default setting is '/'
   * Ex: if you want to proxy the splunk UI at http://splunk:8000/splunkui, then set root_endpoint = /splunkui

static_endpoint = <URI_prefix_string>
   * path to static content
   * The path here is automatically appended to root_endpoint defined above
   * default is /static

static_dir = <relative_filesystem_path>
   * The directory that actually holds the static content
   * This can be an absolute url if you want to put it elsewhere
   * Default is share/splunk/search_mrsparkle/exposed

rss_endpoint = <URI_prefix_string>
   * path to static rss content
   * The path here is automatically appended to root_endpoint defined above
   * default is /rss

tools.staticdir.generate_indexes = [1 | 0]
   * Indicates if the webserver will serve a directory listing for static directories
   * Defaults to 0 (false)

template_dir = <relative_filesystem_path>
   * base path to mako templates
   * Defaults to share/splunk/search_mrsparkle/templates

module_dir = <relative_filesystem_path>
   * base path to UI module assets
   * Defaults to share/splunk/search_mrsparkle/modules
   
enable_gzip = [True | False]
   * Determines if webserver applies gzip compression to responses
   * Defaults to True

use_future_expires = [True | False]
   * Determines if the Expires header of /static files is set to a far-future date
   * Defaults to True

flash_major_version = <integer>
flash_minor_version = <integer>
flash_revision_version = <integer>
   * Specifies the minimum Flash plugin version requirements
   * Flash support, broken into three parts.
   * We currently require a min baseline of Shockwave Flash 9.0 r124

simple_xml_force_flash_charting = [True | False]
   * Specifies whether or not to force the use of FlashChart when rendering simple xml into view xml
   * Defaults to False

enable_proxy_write = [True | False]
   * Indicates if the /splunkd proxy endpoint allows POST operations
   * If True, both GET and POST operations are proxied through to splunkd
   * If False, only GET operations are proxied through to splunkd
   * Setting this to False will prevent many client-side packages (such as the Splunk JavaScript SDK) from working correctly
   * Defaults to True

js_logger_mode = [None | Firebug | Server]
   * JavaScript Logger mode
   * Available modes: None, Firebug, Server
   * Mode None: Does not log anything
   * Mode Firebug: Use firebug by default if it exists or defer to the older less promiscuous version of firebug lite
   * Mode Server: Log to a defined server endpoint
   * See js/logger.js Splunk.Logger.Mode for mode implementation details and if you would like to author your own
   * Defaults to None

js_logger_mode_server_end_point = <URI_relative_path>
   * Specifies the server endpoint to post javascript log messages
   * Used when js_logger_mode = Server
   * Defaults to util/log/js

js_logger_mode_server_poll_buffer = <integer>
   * Specifieds the interval in milliseconds to check, post and cleanse the javascript log buffer
   * Defaults to 1000

js_logger_mode_server_max_buffer = <integer>
   * Specifies the maximum size threshold to post and cleanse the javascript log buffer
   * Defaults to 100

ui_inactivity_timeout = <integer>
   * Specifies the length of time lapsed (in minutes) for notification when there is no user interface clicking, mouseover, scrolling or resizing.
   * Notifies client side pollers to stop, resulting in sessions expiring at the tools.sessions.timeout value.
   * If less than 1, results in no timeout notification ever being triggered (Sessions will stay alive for as long as the browser is open).
   * Defaults to 60 minutes

js_no_cache = [True | False]
   * Toggle js cache control
   * Defaults to False

enable_autocomplete_login = [True | False]
   * Indictes if the main login page allows browsers to autocomplete the username
   * If True, browsers may display an autocomplete drop down in the username field
   * If False, browsers are instructed not to show autocomplete drop down in the username field
   * Defaults to True

minify_js = [True | False]
   * indicates whether the static JS files for modules are consolidated and minified
   * enabling improves client-side performance by reducing the number of HTTP requests and the size of HTTP responses

minify_css = [True | False]
   * indicates whether the static CSS files for modules are consolidated and minified
   * enabling improves client-side performance by reducing the number of HTTP requests and the size of HTTP responses
   * due to browser limitations, disabling this when using IE9 and earlier may result in display problems.

trap_module_exceptions = [True | False]
   * Toggle whether the JS for individual modules is wrapped in a try/catch
   * If True, syntax errors in individual modules will not cause the UI to hang,
   * other than when using the module in question
   * Set this to False when developing apps.
   
jschart_test_mode = [True | False]
   * Toggle whether JSChart module runs in Test Mode
   * If True, JSChart module attaches HTML classes to chart elements for introspection
   * This will negatively impact performance, so should be disabled unless actively in use.

max_view_cache_size = <integer>
    * Specifies the maximum number of views to cache in the appserver.
    * Defaults to 300.

pdfgen_is_available = [0 | 1]
    * Specifies whether Integrated PDF Generation is available on this search head
    * This is used to bypass an extra call to splunkd 
    * Defaults to 1 on platforms where node is supported, defaults to 0 otherwise

version_label_format = <printf_string>
   * internal config
   * used to override the version reported by the UI to *.splunk.com resources
   * defaults to: %s

auto_refresh_views = [0 | 1]
    * Specifies whether the following actions cause the appserver to ask splunkd to reload views from disk.
        * Logging in via the UI
        * Switching apps
        * Clicking the Splunk logo
    * Defaults to 0.
#
# Header options
#
x_frame_options_sameorigin = [True | False]
    * adds a X-Frame-Options header set to "SAMEORIGIN" to every response served by cherrypy
    * Defaults to True

#
# SSO
#

remoteUser = <http_header_string>
   * Remote user HTTP header sent by the authenticating proxy server.
   * This header should be set to the authenticated user.
   * Defaults to 'REMOTE_USER'.
   * Caution: There is a potential security concern regarding Splunk's treatment of HTTP headers.
     * Your proxy provides the selected username as an HTTP header as specified above.
     * If the browser or other http agent were to specify the value of this
       header, probably any proxy would overwrite it, or in the case that the
       username cannot be determined, refuse to pass along the request or set
       it blank.
     * However, Splunk (cherrypy) will normalize headers containing the dash,
       and the underscore to the same value.  For example USER-NAME and
       USER_NAME will be treated as the same in SplunkWeb.
     * This means that if the browser provides REMOTE-USER and splunk accepts
       REMOTE_USER, theoretically the browser could dictate the username.
     * In practice, however, in all our testing, the proxy adds its headers
       last, which causes them to take precedence, making the problem moot.

SSOMode = [permissive | strict]
   * Allows SSO to behave in either permissive or strict mode.
   * Permissive: Requests to Splunk Web that originate from an untrusted IP address 
     are redirected to a login page where they can log into Splunk without using SSO.
   * Strict: All requests to splunkweb will be restricted to those originating
     from a trusted IP except those to endpoints not requiring authentication. 
   * Defaults to "strict"

trustedIP = <ip_address>
   # Trusted IP.  This is the IP address of the authenticating proxy.
   # Splunkweb verifies it is receiving data from the proxy host for all
   # SSO requests.
   # Uncomment and set to a valid IP address to enable SSO.
   # Disabled by default.  Normal value is '127.0.0.1'

testing_endpoint = <relative_uri_path>
   * Specifies the root URI path on which to serve splunkweb unit and 
   * integration testing resources.
   * Development only setting
   * Defaults to '/testing'
   
testing_dir = <relative_file_path>
   * Specifies the path relative to $SPLUNK_HOME that contains the testing
   * files to be served at endpoint defined by 'testing_endpoint'.
   * Development only setting
   * Defaults to 'share/splunk/testing'

#
# cherrypy HTTP server config
#

server.thread_pool = <integer>
   * Specifies the minimum number of threads the appserver is allowed to maintain
   * Defaults to 20

server.thread_pool_max = <integer>
   * Specifies the maximum number of threads the appserver is allowed to maintain
   * Defaults to -1 (unlimited)

server.thread_pool_min_spare = <integer>
    * Specifies the minimum number of spare threads the appserver keeps idle
    * Defaults to 5

server.thread_pool_max_spare = <integer>
    * Specifies the maximum number of spare threads the appserver keeps idle
    * Defaults to 10
   
server.socket_host = <ip_address>
   * Host values may be any IPv4 or IPv6 address, or any valid hostname.
   * The string 'localhost' is a synonym for '127.0.0.1' (or '::1', if
   * your hosts file prefers IPv6). The string '0.0.0.0' is a special
   * IPv4 entry meaning "any active interface" (INADDR_ANY), and '::'
   * is the similar IN6ADDR_ANY for IPv6. 
   * Defaults to 0.0.0.0 if listenOnIPv6 is set to no, else ::

listenOnIPv6 = <no | yes | only>
    * By default, splunkweb will listen for incoming connections using 
      IPv4 only
    * To enable IPv6 support in splunkweb, set this to "yes".  Splunkweb
      will simultaneously listen for connections on both IPv4 and IPv6
    * To disable IPv4 entirely, set this to "only", which will cause splunkweb
      to exclusively accept connections over IPv6.  
    * You will also want to set server.socket_host (use "::" instead of "0.0.0.0")
      if you wish to listen on an IPv6 address

max_upload_size = <integer>
   * Specifies the hard maximum size of uploaded files in MB
   * Defaults to 500

log.access_file = <filename>
   * Specifies the HTTP access log filename
   * Stored in default Splunk /var/log directory
   * Defaults to web_access.log

log.access_maxsize = <integer>
    * Specifies the maximum size the web_access.log file should be allowed to grow to (in bytes)
    * Comment out or set to 0 for unlimited file size
    * File will be rotated to web_access.log.0 after max file size is reached
    * See log.access_maxfiles to limit the number of backup files created
    * Defaults to unlimited file size

log.access_maxfiles = <integer>
    * Specifies the maximum number of backup files to keep after the web_access.log file has reached its maximum size
    * Warning: setting this to very high numbers (eg. 10000) may impact performance during log rotations
    * Defaults to 5 if access_maxsize is set

log.error_maxsize = <integer>
    * Specifies the maximum size the web_service.log file should be allowed to grow to (in bytes)
    * Comment out or set to 0 for unlimited file size
    * File will be rotated to web_service.log.0 after max file size is reached
    * See log.error_maxfiles to limit the number of backup files created
    * Defaults to unlimited file size

log.error_maxfiles = <integer>
    * Specifies the maximum number of backup files to keep after the web_service.log file has reached its maximum size
    * Warning: setting this to very high numbers (eg. 10000) may impact performance during log rotations
    * Defaults to 5 if access_maxsize is set

log.screen = [True | False]
   * Indicates if runtime output is displayed inside an interactive tty
   * Defaults to True
   
request.show_tracebacks = [True | False]
   * Indicates if a an exception traceback is displayed to the user on fatal exceptions
   * Defaults to True

engine.autoreload_on = [True | False]
   * Indicates if the appserver will auto-restart if it detects a python file has changed
   * Defaults to False

tools.sessions.on = True
    * Indicates if user session support is enabled
    * Should always be True

tools.sessions.timeout = <integer>
   * Specifies the number of minutes of inactivity before a user session is expired
   * The countdown is effectively reset by browser activity minute until
     ui_inactivity_timeout inactivity timeout is reached.
   * Use a value of 2 or higher, as a value of 1 will race with the browser
     refresh, producing unpredictable behavior. 
     (Low values aren't very useful though except for testing.)
   * Defaults to 60

tools.sessions.restart_persist = [True | False]
    * If set to False then the session cookie will be deleted from the browser
      when the browser quits
    * Defaults to True - Sessions persist across browser restarts
      (assuming the tools.sessions.timeout limit hasn't been reached)

tools.sessions.httponly = [True | False]
    * If set to True then the session cookie will be made unavailable
      to running javascript scripts, increasing session security
    * Defaults to True

tools.sessions.secure = [True | False]
    * If set to True and Splunkweb is configured to server requests using HTTPS
      (see the enableSplunkWebSSL setting) then the browser will only transmit 
      the session cookie over HTTPS connections, increasing session security
      * Defaults to True

response.timeout = <integer>
   * Specifies the number of seconds to wait for the server to complete a response
   * Some requests such as uploading large files can take a long time
   * Defaults to 7200

tools.sessions.storage_type = [file]
tools.sessions.storage_path = <filepath>
   * Specifies the session information storage mechanisms
   * Comment out the next two lines to use RAM based sessions instead
   * Use an absolute path to store sessions outside of the splunk tree
   * Defaults to storage_type=file, storage_path=var/run/splunk

tools.decode.on = [True | False]
   * Indicates if all strings that come into Cherrpy controller methods are decoded as unicode (assumes UTF-8 encoding).
   * WARNING: Disabling this will likely break the application, as all incoming strings are assumed
   * to be unicode.
   * Defaults to True

tools.encode.on = [True | False]
   * Encodes all controller method response strings into UTF-8 str objects in Python.
   * WARNING: Disabling this will likely cause high byte character encoding to fail.
   * Defaults to True

tools.encode.encoding = <codec>
   * Force all outgoing characters to be encoded into UTF-8.
   * This only works with tools.encode.on set to True.
   * By setting this to utf-8, Cherrypy's default behavior of observing the Accept-Charset header
   * is overwritten and forces utf-8 output. Only change this if you know a particular browser
   * installation must receive some other character encoding (Latin-1 iso-8859-1, etc)
   * WARNING: Change this at your own risk.
   * Defaults to utf08

tools.proxy.on = [True | False]
   * Used for running Apache as a proxy for Splunk UI, typically for SSO configuration. See http://tools.cherrypy.org/wiki/BehindApache for more information.
   * For Apache 1.x proxies only. Set this attribute to "true". This configuration instructs CherryPy (the Splunk Web HTTP server) to look for an incoming X-Forwarded-Host header and to use the value of that header to construct canonical redirect URLs that include the proper host name. For more information, refer to the CherryPy documentation on running behind an Apache proxy. This setting is only necessary for Apache 1.1 proxies. For all other proxies, the setting must be "false", which is the default.
   * Defaults to False

pid_path = <filepath>
   * Specifies the path to the PID file
   * Equals precisely and only var/run/splunk/splunkweb.pid
   * NOTE: Do not change this parameter.

enabled_decomposers = <intention> [, <intention>]...
   * Added in Splunk 4.2 as a short term workaround measure for apps which happen to still require search decomposition, which is deprecated with 4.2.
   * Search decomposition will be entirely removed in a future release.
   * Comma separated list of allowed intentions.
   * Modifies search decomposition, which is a splunk-web internal behavior.
   * Can be controlled on a per-app basis.
   * If set to the empty string, no search decomposition occurs, which causes some usability problems with report builder.
   * The current possible values are: addcommand, stats, addterm, addtermgt, addtermlt, setfields, excludefields, audit, sort, plot 
   * Default is 'plot', leaving only the plot intention enabled.

simple_xml_module_render = [True | False]
  * If True, simple xml dashboards and forms will render using the module system
  * Defaults to False

simple_xml_perf_debug = [True | False]
  * If True, simple xml dashboards will log some performance metrics to the browser console
  * Defaults to False

[framework]
* Put App Framework settings here
django_enable = [True | False]
  * Specifies whether Django should be enabled or not
  * Defaults to True
  * Django will not start unless an app requires it
  
django_path = <filepath>
  * Specifies the root path to the new App Framework files, relative to $SPLUNK_HOME
  * Defaults to etc/apps/framework
  
django_force_enable = [True | False]
  * Specifies whether to force Django to start, even if no app requires it
  * Defaults to False


#
# custom cherrypy endpoints
#

[endpoint:<python_module_name>]
   * registers a custom python CherryPy endpoint
   * the expected file must be located at: $SPLUNK_HOME/etc/apps/<APP_NAME>/appserver/controllers/<PYTHON_NODULE_NAME>.py
   * this module's methods will be exposed at /custom/<APP_NAME>/<PYTHON_NODULE_NAME>/<METHOD_NAME>

