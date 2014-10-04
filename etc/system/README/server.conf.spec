#   Version 6.0
#
# This file contains the set of attributes and values you can use to configure server options
# in server.conf.
#
# There is a server.conf in $SPLUNK_HOME/etc/system/default/.  To set custom configurations, 
# place a server.conf in $SPLUNK_HOME/etc/system/local/.  For examples, see server.conf.example.
# You must restart Splunk to enable configurations.
#
# To learn more about configuration files (including precedence) please see the documentation 
# located at http://docs.splunk.com/Documentation/Splunk/latest/Admin/Aboutconfigurationfiles

# GLOBAL SETTINGS
# Use the [default] stanza to define any global settings.
#     * You can also define global settings outside of any stanza, at the top of the file.
#     * Each conf file should have at most one default stanza. If there are multiple default
#       stanzas, attributes are combined. In the case of multiple definitions of the same
#       attribute, the last definition in the file wins.
#     * If an attribute is defined at both the global level and in a specific stanza, the
#       value in the specific stanza takes precedence.


##########################################################################################
# General Server Configuration
##########################################################################################
[general]
serverName = <ASCII string>
    * The name used to identify this Splunk instance for features such as distributed search.
    * Defaults to <hostname>-<user running splunk>.
    * May not be an empty string
    * May contain environment variables
    * After any environment variables have been expanded, the server name (if not an IPv6
      address) can only contain letters, numbers, underscores, dots, and dashes; and
      it must start with a letter, number, or an underscore.  

sessionTimeout = <nonnegative integer>[smhd]
    * The amount of time before a user session times out, expressed as a search-like time range
    * Examples include '24h' (24 hours), '3d' (3 days), '7200s' (7200 seconds, or two hours)
    * Defaults to '1h' (1 hour)

trustedIP = <IP address>
    * All logins from this IP address are trusted, meaning password is no longer required
    * Only set this if you are using Single Sign On (SSO)

allowRemoteLogin = always|never|requireSetPassword
    * Controls remote management by restricting general login. Note that this does not apply to trusted
      SSO logins from trustedIP.
    * If 'always', enables authentication so that all remote login attempts are allowed.
    * If 'never', only local logins to splunkd will be allowed. Note that this will still allow
      remote management through splunkweb if splunkweb is on the same server.
    * If 'requireSetPassword' (default):
         * In the free license, remote login is disabled.
         * In the pro license, remote login is only disabled for "admin" user if default password of "admin" has not been changed.

pass4SymmKey = <password string>
    * This is prepended to the splunk symmetric key to generate the final key which is used to
      sign all traffic between master/slave licenser

listenOnIPv6 = no|yes|only
    * By default, splunkd will listen for incoming connections (both REST
      and TCP inputs) using IPv4 only
    * To enable IPv6 support in splunkd, set this to 'yes'.  splunkd will simultaneously
      listen for connections on both IPv4 and IPv6
    * To disable IPv4 entirely, set this to 'only', which will cause splunkd
      to exclusively accept connections over IPv6.  You will probably also
      need to change mgmtHostPort in web.conf (use '[::1]' instead of '127.0.0.1')
    * Note that any setting of SPLUNK_BINDIP in your environment or splunk-launch.conf
      will override this value.  In that case splunkd will listen on the exact address
      specified.

connectUsingIpVersion = auto|4-first|6-first|4-only|6-only
    * When making outbound TCP connections (for forwarding eventdata, making
      distributed search requests, etc) this controls whether the connections will
      be made via IPv4 or IPv6.
    * If a host is available over both IPv4 and IPv6 and this is set to '4-first', then
      we will connect over IPv4 first and fallback to IPv6 if the connection fails.
    * If it is set to '6-first' then splunkd will try IPv6 first and fallback to IPv4 on failure
    * If this is set to '4-only' then splunkd will only attempt to make connections over IPv4.
    * Likewise, if this is set to '6-only', then splunkd will only attempt to connect to the IPv6 address.
    * The default value of 'auto' will select a reasonable value based on listenOnIPv6 setting
      If that value is set to 'no' it will act like '4-only'.  If it is set to 'yes' it will
      act like '6-first' and if it is set to 'only' it will act like '6-only'.
    * Note that connections to literal addresses are unaffected by this.  For example,
      if a forwarder is configured to connect to "10.1.2.3" the connection will be made over
      IPv4 regardless of this setting.

guid = <globally unique identifier for this instance>
    * This setting now (as of 5.0) belongs in the [general] stanza of SPLUNK_HOME/etc/instance.cfg file;
      please see specfile of instance.cfg for more information.

useHTTPServerCompression = true|false
    * Whether splunkd HTTP server should support gzip content encoding. For more info on how 
      content encoding works, see http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html (section 14.3).
    * Defaults to true.

defaultHTTPServerCompressionLevel = <integer>
    * If useHTTPServerCompression is enabled, this setting constrols the
      compression "level" we attempt
    * This number must be in the range 1 through 9
    * Higher numbers produce smaller compressed results but require more CPU usage
    * The default value of 6 is appropriate for most environments

skipHTTPCompressionAcl = <network_acl>
    * Lists a set of networks or addresses to skip compressing data for.
      These are addresses that are considered so close that network speed
      is never an issue, so any CPU time spent compressing a response is
      wasteful.
    * Note that the server may still respond with compressed data if it
      already has a compressed version of the data available.
    * These rules are separated by commas or spaces
    * Each rule can be in the following forms:
    *   1. A single IPv4 or IPv6 address (examples: "10.1.2.3", "fe80::4a3")
    *   2. A CIDR block of addresses (examples: "10/8", "fe80:1234/32")
    *   3. A DNS name, possibly with a '*' used as a wildcard (examples: "myhost.example.com", "*.splunk.com")
    *   4. A single '*' which matches anything
    * Entries can also be prefixed with '!' to negate their meaning.
    * Defaults to localhost addresses.

useHTTPClientCompression = true|false|on-http|on-https
    * Whether gzip compression should be supported when Splunkd acts as a client (including distributed searches). Note that  
      in order for the content to be compressed, the HTTP server that the client is connecting to should also support compression.
    * If the connection is being made over https and useClientSSLCompression=true (see below), then setting this 
      option to true would result in double compression work without much compression gain. It is recommended that this
      value be set to on-http (or to true, and useClientSSLCompression to false).
    * Defaults to false.

##########################################################################################
# SSL Configuration details
##########################################################################################

[sslConfig]
    * Set SSL for communications on Splunk back-end under this stanza name.
        * NOTE: To set SSL (eg HTTPS) for Splunk Web and the browser, use web.conf.
    * Follow this stanza name with any number of the following attribute/value pairs.  
    * If you do not specify an entry for each attribute, Splunk will use the default value.

enableSplunkdSSL = true|false
    * Enables/disables SSL on the splunkd management port (8089).
    * Defaults to true.
    * Note: Running splunkd without SSL is not generally recommended. 
    * Distributed search will often perform better with SSL enabled.

useClientSSLCompression = true|false
    * Turns on HTTP client compression. 
    * Server-side compression is turned on by default; setting this on the client side enables 
      compression between server and client.  
    * Enabling this potentially gives you much faster distributed searches across multiple Splunk instances.
    * Defaults to true.
    
 useSplunkdClientSSLCompression = true|false
    * Controls whether SSL compression would be used when splunkd is acting as an HTTP client,
      usually during certificate exchange, bundle replication, remote calls etc. 
    * NOTE: this setting is effective if, and only if, useClientSSLCompression is set to true
    * NOTE: splunkd is not involved in data transfer in distributed search, the search in a separate process is.
    * Defaults to true.
 
supportSSLV3Only = true|false
        * If true, tells the HTTP server to only accept connections
          from SSLv3 clients.
        * Default is false.

sslVerifyServerCert = true|false
        * Used by distributed search: when making a search request to another
          server in the search cluster.
        * Used by distributed deployment clients: when polling a deployment
          server.
        * If this is set to true, you should make sure that the server that is
          being connected to is a valid one (authenticated).  Both the common
          name and the alternate name of the server are then checked for a
          match if they are specified in this configuration file.  A
          certificiate is considered verified if either is matched.
        * Default is false.

sslCommonNameToCheck = <commonName>
        * If this value is set, and 'sslVerifyServerCert' is set to true,
          splunkd will limit most outbound HTTPS connections to hosts which use
          a cert with this common name. 
        * 'sslCommonNameList' is a multivalue extension of this setting, certs
          which match 'sslCommonNameList' or 'sslCommonNameToCheck' will be
          accepted.
        * The most important scenario is distributed search.
        * This feature does not work with the deployment server and client
          communication over SSL.
        * Optional.  Defaults to no common name checking.

sslCommonNameList = <commonName1>, <commonName2>, ...
        * If this value is set, and 'sslVerifyServerCert' is set to true,
          splunkd will limit most outbound HTTPS connections to hosts which use
          a cert with one of the listed common names. 
        * The most important scenario is distributed search.
        * Optional.  Defaults to no common name checking.

sslAltNameToCheck = <alternateName1>, <alternateName2>, ...
        * If this value is set, and 'sslVerifyServerCert' is set to true,
          splunkd will also be willing to verify certificates which have a
          so-called "Subject Alternate Name" that matches any of the alternate
          names in this list.
            * Subject Alternate Names are effectively extended descriptive
              fields in SSL certs beyond the commonName.  A common practice for
              HTTPS certs is to use these values to store additional valid
              hostnames or domains where the cert should be considered valid.
        * Accepts a comma-separated list of Subject Alternate Names to consider
          valid.
        * Items in this list are never validated against the SSL Common Name.
        * This feature does not work with the deployment server and client
          communication over SSL.
        * Optional.  Defaults to no alternate name checking

requireClientCert = true|false
        * Requires that any HTTPS client that connects to splunkd internal HTTPS server
        has a certificate that was signed by our CA (certificate authority).
        * Used by distributed search: Splunk indexing instances must be authenticated
        to connect to another splunk indexing instance.
        * Used by distributed deployment: the deployment server requires that 
        deployment clients are authenticated before allowing them to poll for new
        configurations/applications.
        * If true, a client can connect ONLY if a certificate created by our
        certificate authority was used on that client.
        * Default is false.

cipherSuite = <cipher suite string>
        * If set, Splunk uses the specified cipher string for the HTTP server.
        * If not set, Splunk uses the default cipher string
         provided by OpenSSL.  This is used to ensure that the server does not
         accept connections using weak encryption protocols.
          
sslKeysfile = <filename>
        * Server certificate file. 
        * Certificates are auto-generated by splunkd upon starting Splunk.
        * You may replace the default cert with your own PEM format file.
        * Certs are stored in caPath (see below).
        * Default is server.pem.
        
sslKeysfilePassword = <password>
        * Server certificate password.
        * Default is password.

caCertFile = <filename>
        * Public key of the signing authority.
        * Default is cacert.pem.

caPath = <path>
        * Path where all these certs are stored.
        * Default is $SPLUNK_HOME/etc/auth.
        
certCreateScript = <script name>
        * Creation script for generating certs on startup 
          of Splunk.

sendStrictTransportSecurityHeader = true|false
        * If set to true, the REST interface will send a "Strict-Transport-Security"
          header with all responses to requests made over SSL.
        * This can help avoid a client being tricked later by a Man-In-The-Middle
          attack to accept a non-SSL request.  However, this requires a commitment that
          no non-SSL web hosts will ever be run on this hostname on any port.  For example,
          if splunkweb is in default non-SSL mode this can break the browser's ability
          to connect to it.  Enable with caution.
        * Defaults to false

allowSslCompression = true|false
        * If set to true, the server will allow clients to negotiate
          SSL-layer data compression.
        * Defaults to false.  The HTTP layer has its own compression layer
          which is usually sufficient.

allowSslRenegotiation = true|false
        * In the SSL protocol, a client may request renegotiation of the connection
          settings from time to time.
        * Setting this to false causes the server to reject all renegotiation
          attempts, breaking the connection.  This limits the amount of CPU a
          single TCP connection can use, but it can cause connectivity problems
          especially for long-lived connections.
        * Defaults to true.

##########################################################################################
# Splunkd HTTP server configuration
##########################################################################################

[httpServer]
    * Set stand-alone HTTP settings for Splunk under this stanza name.
    * Follow this stanza name with any number of the following attribute/value pairs.  
    * If you do not specify an entry for each attribute, Splunk uses the default value.

atomFeedStylesheet = <string>
    * Defines the stylesheet relative URL to apply to default Atom feeds.
    * Set to 'none' to stop writing out xsl-stylesheet directive.  
    * Defaults to /static/atom.xsl.

max-age = <nonnegative integer>
    * Set the maximum time (in seconds) to cache a static asset served off of the '/static' directory.
    * This value is passed along in the 'Cache-Control' HTTP header.
    * Defaults to 3600.
          
follow-symlinks = true|false
    * Toggle whether static file handler (serving the '/static' directory) follow filesystem 
      symlinks when serving files.  
    * Defaults to false.
          
disableDefaultPort = true|false
        * If true, turns off listening on the splunkd management port (8089 by default)
        * Default value is 'false'.

acceptFrom = <network_acl> ...
    * Lists a set of networks or addresses to accept data from.  These rules are separated by commas or spaces
    * Each rule can be in the following forms:
    *   1. A single IPv4 or IPv6 address (examples: "10.1.2.3", "fe80::4a3")
    *   2. A CIDR block of addresses (examples: "10/8", "fe80:1234/32")
    *   3. A DNS name, possibly with a '*' used as a wildcard (examples: "myhost.example.com", "*.splunk.com")
    *   4. A single '*' which matches anything
    * Entries can also be prefixed with '!' to cause the rule to reject the
      connection.  Rules are applied in order, and the first one to match is
      used.  For example, "!10.1/16, *" will allow connections from everywhere
      except the 10.1.*.* network.
    * Defaults to "*" (accept from anywhere)

streamInWriteTimeout = <positive number>
        * When uploading data to http server, if http server is unable to write data to
        * receiver for configured streamInWriteTimeout seconds, it aborts write operation.
        * Defaults to 5 seconds.

max_content_length = <int>
        * Measured in bytes
        * HTTP requests over this size will rejected.
        * Exists to avoid allocating an unreasonable amount of memory from web requests
        * Defaulted to 838860800 or 800MB
        * In environments where indexers have enormous amounts of RAM, this
          number can be reasonably increased to handle large quantities of
          bundle data.

maxThreads = <int>
        * Number of threads that can be used by active HTTP transactions.
          This can be limited to constrain resource usage.
        * If set to 0 (the default) a limit will be automatically picked
          based on estimated server capacity.
        * If set to a negative number, no limit will be enforced.

maxSockets = <int>
        * Number of simultaneous HTTP connections that we'll accept simultaneously.
          This can be limited to constrain resource usage.
        * If set to 0 (the default) a limit will be automatically picked
          based on estimated server capacity.
        * If set to a negative number, no limit will be enforced.

forceHttp10 = auto|never|always
        * When set to "always", the REST HTTP server will not use some
          HTTP 1.1 features such as persistent connections or chunked
          transfer encoding.
        * When set to "auto" it will do this only if the client sent no
          User-Agent header, or if the user agent is known to have bugs
          in its HTTP/1.1 support.
        * When set to "never" it always will allow HTTP 1.1, even to
          clients it suspects may be buggy.
        * Defaults to "auto"

crossOriginSharingPolicy = <origin_acl> ...
        * List of HTTP Origins to return Access-Control-Allow-* (CORS) headers for
        * These headers tell browsers that we trust web applications at those sites
          to make requests to the REST interface
        * The origin is passed as a URL without a path component (for example
          "https://app.example.com:8000")
        * This setting can take a list of acceptable origins, separated
          by spaces and/or commas
        * Each origin can also contain wildcards for any part.  Examples:
            *://app.example.com:*  (either HTTP or HTTPS on any port)
            https://*.example.com  (any host under example.com, including example.com itself)
        * An address can be prefixed with a '!' to negate the match, with
          the first matching origin taking precedence.  For example,
          "!*://evil.example.com:* *://*.example.com:*" to not avoid
          matching one host in a domain
        * A single "*" can also be used to match all origins
        * By default the list is empty

x_frame_options_sameorigin = true|false
        * adds a X-Frame-Options header set to "SAMEORIGIN" to every response served by splunkd
        * Defaults to true

cliLoginBanner = <string>
        * Sets a message which will be added to the HTTP reply headers
          of requests for authentication, and to the "server/info" endpoint
        * This will be printed by the Splunk CLI before it prompts
          for authentication credentials.  This can be used to print
          access policy information.
        * If this string starts with a '"' character, it is treated as a
          CSV-style list with each line comprising a line of the message.
          For example: "Line 1","Line 2","Line 3"
        * Defaults to empty (no message)

allowBasicAuth = true|false
        * Allows clients to make authenticated requests to the splunk
          server using "HTTP Basic" authentication in addition to the
          normal "authtoken" system
        * This is useful for programmatic access to REST endpoints and
          for accessing the REST API from a web browser.  It is not
          required for the UI or CLI.
        * Defaults to true

basicAuthRealm = <string>
        * When using "HTTP Basic" authenitcation, the 'realm' is a
          human-readable string describing the server.  Typically, a web
          browser will present this string as part of its dialog box when
          asking for the username and password.
        * This can be used to display a short message describing the
          server and/or its access policy.
        * Defaults to "/splunk"

#########################################################################################
# Splunkd HTTPServer listener configuration
#########################################################################################

[httpServerListener:<ip>:<port>]
        * Enable the splunkd http server to listen on a network interface (NIC) specified by
        <ip> and a port number specified by <port>.  If you leave <ip> blank (but still include the ':'),
        splunkd will listen on the kernel picked NIC using port <port>.

ssl = true|false
        * Toggle whether this listening ip:port will use SSL or not.
        * Default value is 'true'.
          
listenOnIPv6 = no|yes|only
        * Toggle whether this listening ip:port will listen on IPv4, IPv6, or both
        * If not present, the setting in the [general] stanza will be used

acceptFrom = <network_acl> ...
    * Lists a set of networks or addresses to accept data from.  These rules are separated by commas or spaces
    * Each rule can be in the following forms:
    *   1. A single IPv4 or IPv6 address (examples: "10.1.2.3", "fe80::4a3")
    *   2. A CIDR block of addresses (examples: "10/8", "fe80:1234/32")
    *   3. A DNS name, possibly with a '*' used as a wildcard (examples: "myhost.example.com", "*.splunk.com")
    *   4. A single '*' which matches anything
    * Entries can also be prefixed with '!' to cause the rule to reject the
      connection.  Rules are applied in order, and the first one to match is
      used.  For example, "!10.1/16, *" will allow connections from everywhere
      except the 10.1.*.* network.
    * Defaults to the setting in the [httpServer] stanza above

##########################################################################################
# Static file handler MIME-type map
##########################################################################################

[mimetype-extension-map]
    * Map filename extensions to MIME type for files served from the static file handler under
    this stanza name.
    
<file-extension> = <MIME-type>
    * Instructs the HTTP static file server to mark any files ending in 'file-extension' 
         with a header of 'Content-Type: <MIME-type>'.
    * Defaults to:
    
    [mimetype-extension-map]
    gif = image/gif
    htm = text/html
    jpg = image/jpg
    png = image/png
    txt = text/plain
    xml = text/xml
    xsl = text/xml
    
##########################################################################################
# Remote applications configuration (e.g. SplunkBase)
##########################################################################################

[applicationsManagement]
    * Set remote applications settings for Splunk under this stanza name.
    * Follow this stanza name with any number of the following attribute/value pairs.  
    * If you do not specify an entry for each attribute, Splunk uses the default value.

allowInternetAccess = true|false
    * Allow Splunk to access the remote applications repository.

url = <URL>
    * Applications repository.
    * Defaults to https://splunkbase.splunk.com/api/apps

loginUrl = <URL>
    * Applications repository login.
    * Defaults to https://splunkbase.splunk.com/api/account:login/

detailsUrl = <URL>
    * Base URL for application information, keyed off of app ID.
    * Defaults to https://splunkbase.splunk.com/apps/id

useragent = <splunk-version>-<splunk-build-num>-<platform>
    * User-agent string to use when contacting applications repository.
    * <platform> includes information like operating system and CPU architecture.

updateHost = <URL>
    * Host section of URL to check for app updates, e.g. https://splunkbase.splunk.com

updatePath = <URL>
    * Path section of URL to check for app updates, e.g. /api/apps:resolve/checkforupgrade

updateTimeout = <time range string>
    * The minimum amount of time Splunk will wait between checks for app updates
    * Examples include '24h' (24 hours), '3d' (3 days), '7200s' (7200 seconds, or two hours)
    * Defaults to '24h'

##########################################################################################
# Misc. configuration
##########################################################################################

[scripts]

initialNumberOfScriptProcesses = <num>
        * The number of pre-forked script processes that are launched
        when the system comes up.  These scripts are reused when script REST endpoints *and*
        search scripts are executed.  The idea is to eliminate the performance
        overhead of launching the script interpreter every time it is invoked.  These
        processes are put in a pool.  If the pool is completely busy when a script gets
        invoked, a new processes is fired up to handle the new invocation - but it 
        disappears when that invocation is finished.


##########################################################################################
# Disk usage settings (for the indexer, not for Splunk log files)
##########################################################################################

[diskUsage]

minFreeSpace = <num>
        * Specified in megabytes.
        * The default setting is 2000 (approx 2GB)
        * Specifies a safe amount of space that must exist for splunkd to continue operating.
        * Note that this affects search and indexing
        * This is how the searching is affected:
        * For search:
            * Before attempting to launch a search, splunk will require this
              amount of free space on the filesystem where the dispatch
              directory is stored, $SPLUNK_HOME/var/run/splunk/dispatch
            * Applied similarly to the search quota values in
              authorize.conf and limits.conf.
        * For indexing: 
            * Periodically, the indexer will check space on all partitions
              that contain splunk indexes as specified by indexes.conf.  Indexing
              will be paused and a ui banner + splunkd warning posted to indicate
              need to clear more disk space.

pollingFrequency = <num>
        * After every pollingFrequency events indexed, the disk usage is checked.
        * The default frequency is every 100000 events.

pollingTimerFrequency = <num>
        * After every pollingTimerFrequency seconds, the disk usage is checked
        * The default value is 10 seconds

##########################################################################################
# Queue settings
##########################################################################################
[queue]

maxSize = [<integer>|<integer>[KB|MB|GB]]
        * Specifies default capacity of a queue.
        * If specified as a lone integer (for example, maxSize=1000), maxSize indicates the maximum number of events allowed
          in the queue.
        * If specified as an integer followed by KB, MB, or GB (for example, maxSize=100MB), it indicates the maximum
          RAM allocated for queue.
        * The default is 500KB.

cntr_1_lookback_time = [<integer>[s|m]] 
        * The lookback counters are used to track the size and count (number of elements in the queue) variation of the queues using an 
          exponentially moving weighted average technique. Both size and count variation has 3 sets of counters each. The set
          of 3 counters is provided to be able to track short, medium and long term history of size/count variation. The user can
          customize the value of these counters or lookback time.
        * Specifies how far into history should the size/count variation be tracked for counter 1.
        * It needs to be specified via an integer followed by [s|m] which stands for seconds and minutes respectively.
        * The default value for counter 1 is set to 60 seconds.

cntr_2_lookback_time = [<integer>[s|m]]
        * See above for explanation and usage of the lookback counter.
        * Specifies how far into history should the size/count variation be tracked for counter 2.
        * The default value for counter 2 is set to 600 seconds.

cntr_3_lookback_time = [<integer>[s|m]]
        * See above for explanation and usage of the lookback counter..
        * Specifies how far into history should the size/count variation be tracked for counter 3.
        * The default value for counter 3 is set to 900 seconds.

sampling_interval = [<integer>[s|m]]
        * The lookback counters described above collects the size and count measurements for the queues.
          This specifies at what interval the measurement collection will happen. Note that for a particular
          queue all the counters sampling interval is same. 
        * It needs to be specified via an integer followed by [s|m] which stands for seconds and minutes respectively.
        * The default sampling_interval value is 1 second.

[queue=<queueName>]

maxSize = [<integer>|<integer>[KB|MB|GB]]
        * Specifies the capacity of a queue. It overrides the default capacity specified in [queue].
        * If specified as a lone integer (for example, maxSize=1000), maxSize indicates the maximum number of events allowed
          in the queue.
        * If specified as an integer followed by KB, MB, or GB (for example, maxSize=100MB), it indicates the maximum
          RAM allocated for queue.
        * The default is inherited from maxSize value specified in [queue]

cntr_1_lookback_time = [<integer>[s|m]] 
        * Same explanation as mentioned in [queue].
        * Specifies the lookback time for the specific queue for counter 1.
        * The default value is inherited from cntr_1_lookback_time value specified in [queue].

cntr_2_lookback_time = [<integer>[s|m]]
        * Specifies the lookback time for the specific queue for counter 2.
        * The default value is inherited from cntr_2_lookback_time value specified in [queue].

cntr_3_lookback_time = [<integer>[s|m]]
        * Specifies the lookback time for the specific queue for counter 3.
        * The default value is inherited from cntr_3_lookback_time value specified in [queue].

sampling_interval = [<integer>[s|m]]
        * Specifies the sampling interval for the specific queue.
        * The default value is inherited from sampling_interval value specified in [queue].

##########################################################################################
# PubSub server settings for the http endpoint.
##########################################################################################

[pubsubsvr-http]

disabled = true|false
    * If disabled, then http endpoint is not registered. Set this value to 'false' to 
        expose PubSub server on http.
    * Defaults to 'true'

stateIntervalInSecs = <seconds>
    * The number of seconds before a connection is flushed due to inactivity. The connection is not
        closed, only messages for that connection are flushed.
    * Defaults to 300 seconds (5 minutes).

##########################################################################################
# General file input settings.
##########################################################################################

[fileInput]

outputQueue = <queue name>
    * The queue that input methods should send their data to.  Most users will not need to
      change this value.
    * Defaults to parsingQueue.

##########################################################################################
# Settings controlling the behavior of 'splunk diag', the diagnostic tool
##########################################################################################

[diag]

EXCLUDE-<class> = <glob expression>
    * Specifies a glob / shell pattern to be excluded from diags generated on this instance. 
    * Example: */etc/secret_app/local/*.conf

##########################################################################################
# License manager settings for configuring the license pool(s)
##########################################################################################

[license]
master_uri = [self|<uri>] 
    * An example of <uri>: <scheme>://<hostname>:<port>
active_group = Enterprise | Trial | Forwarder | Free
# these timeouts only matter if you have a master_uri set to remote master
connection_timeout = 30
    * Maximum time (in seconds) to wait before connection to master times out
send_timeout = 30
    * Maximum time (in seconds) to wait before sending data to master times out
receive_timeout = 30
    * Maximum time (in seconds) to wait before receiving data from master times out

squash_threshold = <positive integer>
    * Advanced setting.  Periodically the indexer must report to license manager the
    data indexed broken down by source, sourcetype, host, and index.  If the number of distinct
    (source,sourcetype,host,index) tuples grows over the squash_threshold, we squash the
    {host,source} values and only report a breakdown by {sourcetype,index}.  This is to
    prevent explosions in memory + license_usage.log lines.  Set this only
    after consulting a Splunk Support engineer.
    * Default: 2000

[lmpool:auto_generated_pool_forwarder]
    * This is the auto generated pool for the forwarder stack

description = <textual description of this license pool>
quota = MAX|<maximum amount allowed by this license>
    * MAX indicates the total capacity of the license. You may have only 1 pool with MAX size in a stack
    * The quota can also be specified as a specific size eg. 20MB, 1GB etc
slaves = *|<slave list>
    * An asterix(*) indicates that any slave can connect to this pool
    * You can also specifiy a comma separated slave guid list
stack_id = forwarder
    * the stack to which this pool belongs

[lmpool:auto_generated_pool_free]
    * This is the auto generated pool for the free stack
    * field descriptions are the same as that for the "lmpool:auto_generated_pool_forwarder"

[lmpool:auto_generated_pool_enterprise]
    * This is the auto generated pool for the enterprise stack
    * field descriptions are the same as that for the "lmpool:auto_generated_pool_forwarder"

[lmpool:auto_generated_pool_fixed-sourcetype_<sha256 hash of srctypes>]
    * This is the auto generated pool for the enterprise fixed srctype stack
    * field descriptions are the same as that for the "lmpool:auto_generated_pool_forwarder"

[lmpool:auto_generated_pool_download_trial]
    * This is the auto generated pool for the download trial stack
    * field descriptions are the same as that for the "lmpool:auto_generated_pool_forwarder"

#########################################################################################
#
# Search head pooling configuration
#
# Changes to a search head's pooling configuration must be made to:
#
#     $SPLUNK_HOME/etc/system/local/server.conf
#
# In other words, you may not deploy the [pooling] stanza via an app, either on
# local disk or on shared storage.
#
# This is because these values are read before the configuration system itself
# has been completely initialized. Take the value of "storage", for example.
# This value cannot be placed within an app on shared storage because Splunk
# must use this value to find shared storage in the first place!
#
##########################################################################################

[pooling]

state = [enabled|disabled]
    * Enables or disables search head pooling.
    * Defaults to disabled.

storage = <path to shared storage>
    * All members of a search head pool must have access to shared storage.
    * Splunk will store configurations and search artifacts here.
    * On *NIX, this should be an NFS mount.
    * On Windows, this should be a UNC path to a Samba/CIFS share.

app_update_triggers = true|false|silent
    * Should this search head run update triggers for apps modified by other
      search heads in the pool?
    * For more information about update triggers specifically, see the
      [triggers] stanza in $SPLUNK_HOME/etc/system/README/app.conf.spec.
    * If set to true, this search head will attempt to reload inputs, indexes,
      custom REST endpoints, etc. stored within apps that are installed,
      updated, enabled, or disabled by other search heads.
    * If set to false, this search head will not run any update triggers. Note
      that this search head will still detect configuration changes and app
      state changes made by other search heads. It simply won't reload any
      components within Splunk that might care about those changes, like input
      processors or the HTTP server.
    * Setting a value of "silent" is like setting a value of "true", with one
      difference: update triggers will never result in restart banner messages
      or restart warnings in the UI. Any need to restart will instead by
      signaled only by messages in splunkd.log.
    * Defaults to true.

lock.timeout = <time range string>
    * Timeout for acquiring file-based locks on configuration files.
    * Splunk will wait up to this amount of time before aborting a configuration write.
    * Defaults to '10s' (10 seconds).

lock.logging = true|false
    * When acquiring a file-based lock, log information into the locked file.
    * This information typically includes:
        * Which host is acquiring the lock
        * What that host intends to do while holding the lock
    * There is no maximum filesize or rolling policy for this logging. If you
      enable this setting, you must periodically truncate the locked file
      yourself to prevent unbounded growth.
    * The information logged to the locked file is intended for debugging
      purposes only. Splunk makes no guarantees regarding the contents of the
      file. It may, for example, write padding NULs to the file or truncate the
      file at any time.
    * Defaults to false.

# The following two intervals interelate; the longest possible time for a state
# change to travel from one search pool member to the rest should be
# approximately the sum of these two timers.
poll.interval.rebuild = <time range string>
    * Rebuild or refresh in-memory configuration data structures at most this often.
    * Defaults to '1m' (1 minute).

poll.interval.check = <time range string>
    * Check on-disk configuration files for changes at most this often.
    * Defaults to '1m' (1 minute).

poll.blacklist.<name> = <regex>
    * Do not check configuration files for changes if they match this regular expression.
    * Example: Do not check vim swap files for changes -- .swp$


##########################################################################################
# High availability clustering configuration
##########################################################################################

[clustering]

mode = [master|slave|searchhead|disabled]
    * Sets operational mode for this cluster node.
    * Only one master may exist per cluster.
    * Defaults to disabled.

master_uri = [<uri> | clustermaster:stanzaName1, clustermaster:stanzaName2]
    * Only valid for mode=slave or searchhead
    * uri of the cluster master that this slave or searchhead should connect to.
    * An example of <uri>: <scheme>://<hostname>:<port>
    * Only for mode=searchhead - If the searchhead is a part of multiple clusters,
    * the master uris can be specified by a comma separated list.

pass4SymmKey = <string>
    * Secret shared among the nodes in the cluster to prevent any
      arbitrary node from connecting to the cluster. If a slave or
      searchhead is not configured with the same secret as the master,
      it will not be able to communicate with the master.
    * Not set by default.
    * If it is not set in the clustering stanza, the key will be looked in
      the general stanza

cxn_timeout = <seconds>
    * Lowlevel timeout for establishing connection between cluster nodes.
    * Defaults to 60s.

send_timeout = <seconds>
    * Lowlevel timeout for sending data between cluster nodes.
    * Defaults to 60s.

rcv_timeout = <seconds>
    * Lowlevel timeout for receiving data between cluster nodes.
    * Defaults to 60s.

rep_cxn_timeout = <seconds>
    * Lowlevel timeout for establishing connection for replicating data.
    * Defaults to 5s.

rep_send_timeout = <seconds>
    * Lowlevel timeout for sending replication slice data between cluster nodes.
    * This is a soft timeout. When this timeout is triggered on source peer, 
      it tries to determine if target is still alive. If it is still alive, 
      it reset the timeout for another rep_send_timeout interval and continues.
      If target has failed or cumulative timeout has exceeded rep_max_send_timeout,
      replication fails.
    * Defaults to 5s.

rep_rcv_timeout = <seconds>
    * Lowlevel timeout for receiving acknowledgement data from peers.
    * This is a soft timeout. When this timeout is triggered on source peer, 
      it tries to determine if target is still alive. If it is still alive, 
      it reset the timeout for another rep_send_timeout interval and continues.
      If target has failed or cumulative timeout has exceeded rep_max_rcv_timeout,
      replication fails.
    * Defaults to 10s.

search_files_retry_timeout = <seconds>
    * Timeout after which request for search files from a peer is aborted.
    * To make a bucket searchable, search specific files are copied from another 
      source peer with search files. If search files on source peers are undergoing
      chances, it asks requesting peer to retry after some time. If cumulative
      retry period exceeds specified timeout, the requesting peer aborts the request and
      requests search files from another peer in the cluster that may have search files.
    * Defaults to 600s.

rep_max_send_timeout = <seconds>
    * Maximum send timeout for sending replication slice data between cluster nodes.
    * On rep_send_timeout source peer determines if total send timeout has exceeded
      rep_max_send_timeout. If so, replication fails.
    * If cumulative rep_send_timeout exceeds rep_max_send_timeout, replication fails.
    * Defaults to 600s.

rep_max_rcv_timeout = <seconds>
    * Maximum cumulative receive timeout for receiving acknowledgement data from peers.
    * On rep_rcv_timeout source peer determines if total receive timeout has exceeded
      rep_max_rcv_timeout. If so, replication fails.
    * Defaults to 600s.

replication_factor = <positive integer>
    * Only valid for mode=master.
    * Determines how many copies of rawdata are created in the cluster.
    # Set this to N, where N is how many peers you have.
    * Must be greater than 0.
    * Defaults to 3

search_factor = <positive integer>
    * Only valid for mode=master 
    * Determines how many buckets will have index structures pre-built.
    * Must be less than or equal to replication_factor and greater than 0.
    * Defaults to 2.

heartbeat_timeout = <positive integer>
    * Only valid for mode=master
    * Determines when the master considers a slave down.  Once a slave
      is down, the master will initiate fixup steps to replicate
      buckets from the dead slave to its peers.
    * Defaults to 60s.

restart_timeout = <positive integer>
    * Only valid for mode=master
    * This is the amount of time the master waits for a peer to come
      back when the peer is restarted (to avoid the overhead of
      trying to fixup the buckets that were on the peer).
    * Note that currently this only works if the peer is restarted vi the UI.

quiet_period = <positive integer>
    * Only valid for mode=master
    * This determines the amount of time for which the master is quiet
      right after it starts. During this period the master does not
      initiate any action but is instead waiting for the slaves to
      register themselves. At the end of this time period, it builds
      its view of the cluster based on the registered information and
      starts normal processing.
    * Defaults to 60s.
      
generation_poll_interval = <positive integer>
    * Only valid if mode=master or mode=searchhead
    * Determines how often the searchhead polls the master for generation information.
    * Defaults to 60s.

max_peer_build_load = <integer>
    * This is the maximum number of concurrent tasks to make buckets
      searchable that can be assigned to a peer.
    * Defaults to 2.

max_peer_rep_load = <integer>
    * This is the maximum number of concurrent non-streaming
      replications that a peer can take part in as a target.
    * Defaults to 5.

max_replication_errors = <integer>
    * Currently only valid for mode=slave
    * This is the maximum number of consecutive replication errors
      (currently only for hot bucket replication) from a source peer
      to a specific target peer. Until this limit is reached, the
      source continues to roll hot buckets on streaming failures to
      this target. After the limit is reached, the source will no
      longer roll hot buckets if streaming to this specific target
      fails. This is reset if at least one successful (hot bucket)
      replication occurs to this target from this source.
    * Defaults to 3.
    * The special value of 0 turns off this safeguard; so the source
      always rolls hot buckets on streaming error to any target.

searchable_targets = true|false
    * Only valid for mode=master
    * Tells the master to make some replication targets searchable
      even while the replication is going on. This only affects
      hot bucket replication for now.
    * Defaults to true

target_wait_time = <positive integer>
    * Only valid for mode=master.
    * Specifies the time that the master waits for the target of a replication to
      register itself before it services the bucket again and potentially schedules
      another fixup.
    * Defaults to 150s

commit_retry_time = <positive integer>
    * Only valid for mode=master
    * Specifies the interval after which, if the last generation commit failed,
      the master forces a retry. A retry is usually automatically kicked off
      after the appropriate events. This is just a backup to make sure that the
       master does retry no matter what.
    * Defaults to 300s

percent_peers_to_restart = <integer between 0-100>
    * suggested percentage of maximum peers to restart for rolling-restart
    * actual percentage may vary due to lack of granularity for smaller peer sets
    * regardless of setting, a minimum of 1 peer will be restarted per round

register_replication_address = <IP address, or fully qualified machine/domain name>
    * Only valid for mode=slave
    * This is the address on which a slave will be available for accepting
      replication data. This is useful in the cases where a slave host machine 
      has multiple interfaces and only one of them can be reached by another 
      splunkd instance
    
register_forwarder_address = <IP address, or fully qualified machine/domain name>
    * Only valid for mode=slave
    * This is the address on which a slave will be available for accepting
      data from forwarder.This is useful in the cases where a splunk host machine 
      has multiple interfaces and only one of them can be reached by another 
      splunkd instance.
 
register_search_address = <IP address, or fully qualified machine/domain name>
    * Only valid for mode=slave
    * This is the address on which a slave will be available as search head.
      This is useful in the cases where a splunk host machine has multiple 
      interfaces and only one of them can be reached by another splunkd instance.

executor_workers = <positive integer>
    * Only valid if mode=master or mode=slave
    * Number of threads that can be used by the clustering threadpool.
    * Defaults to 10. A value of 0 will default to 1.

heartbeat_period = <non-zero positive integer>
    * Only valid for mode=slave
    * Controls the frequency the slave attempts to send heartbeats

enableS2SHeartbeat = true|false
    * Only valid for mode=slave
    * Splunk will monitor each replication connection for presence of heartbeat, 
      and if the heartbeat is not seen for s2sHeartbeatTimeout seconds, it will 
      close the connection.
    * Defaults to true.

s2sHeartbeatTimeout = <seconds>
   * This specifies the global timeout value for monitoring heartbeats on replication connections.
   * Splunk will will close a replication connection if heartbeat is not seen for s2sHeartbeatTimeout seconds.
   * Defaults to 600 seconds (10 minutes). Replication source sends heartbeat every 30 second.

[clustermaster:stanza1]
   * Only valid for mode=searchhead when the searchhead is a part of multiple clusters.

master_uri = <uri>
    * Only valid for mode=searchhead when present in this stanza.
    * uri of the cluster master that this searchhead should connect to.

pass4SymmKey = <string>
    * Secret shared among the nodes in the cluster to prevent any
      arbitrary node from connecting to the cluster. If a searchhead
      is not configured with the same secret as the master,
      it will not be able to communicate with the master.
    * Not set by default.
    * If it is not present here, the key in the clustering stanza will be used. If it is not present 
      in the clustering stanza, the value in the general stanza will be used.

[replication_port://<port>]
    # Configure Splunk to listen on a given TCP port for replicated data from another cluster member.
    # If mode=slave is set in the [clustering] stanza at least one replication_port must be configured and not disabled.

disabled = true|false
    * Set to true to disable this replication port stanza.
    * Defaults to false.

listenOnIPv6 = no|yes|only
    * Toggle whether this listening port will listen on IPv4, IPv6, or both.
    * If not present, the setting in the [general] stanza will be used.

acceptFrom = <network_acl> ...
    * Lists a set of networks or addresses to accept connections from.  These rules are separated by commas or spaces
    * Each rule can be in the following forms:
    *   1. A single IPv4 or IPv6 address (examples: "10.1.2.3", "fe80::4a3")
    *   2. A CIDR block of addresses (examples: "10/8", "fe80:1234/32")
    *   3. A DNS name, possibly with a '*' used as a wildcard (examples: "myhost.example.com", "*.splunk.com")
    *   4. A single '*' which matches anything
    * Entries can also be prefixed with '!' to cause the rule to reject the
      connection.  Rules are applied in order, and the first one to match is
      used.  For example, "!10.1/16, *" will allow connections from everywhere
      except the 10.1.*.* network.
    * Defaults to "*" (accept replication data from anywhere)

[replication_port-ssl://<port>]
    * This configuration is same as replication_port stanza above but uses SSL.

disabled = true|false
    * Set to true to disable this replication port stanza.
    * Defaults to false.

listenOnIPv6 = no|yes|only
    * Toggle whether this listening port will listen on IPv4, IPv6, or both.
    * If not present, the setting in the [general] stanza will be used.

acceptFrom = <network_acl> ...
    * This setting is same as setting in replication_port stanza defined above.

serverCert = <path>
    * Full path to file containing private key and server certificate.
    * There is no default value.
    
password = <string>
    * Server certificate password, if any.
    * There is no default value.

rootCA = <string>
    * The path to the file containing the SSL certificate for root certifying authority.
    * The file may also contain root and intermediate certificates, if required.
    * There is no default value.

cipherSuite = <cipher suite string>
    * If set, uses the specified cipher string for the SSL connection.
    * If not set, uses the default cipher string.
    * provided by OpenSSL.  This is used to ensure that the server does not
      accept connections using weak encryption protocols.

supportSSLV3Only = true|false
    * If true, it only accept connections from SSLv3 clients.
    * Default is false.

compressed = true|false
    * If true, it enables compression on SSL.
    * Default is true.

requireClientCert = true|false
    * Requires that any peer that connects to replication port has a certificate that
      can be validated by certificate authority specified in rootCA.
    * Default is false.

allowSslRenegotiation = true|false
    * In the SSL protocol, a client may request renegotiation of the connection
      settings from time to time.
    * Setting this to false causes the server to reject all renegotiation
      attempts, breaking the connection.  This limits the amount of CPU a
      single TCP connection can use, but it can cause connectivity problems
      especially for long-lived connections.
    * Defaults to true.
