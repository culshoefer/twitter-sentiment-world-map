module Lib where

import Web.Twitter.Conduit
import Data.ByteString.Char8 (pack)
import qualified Constants as C

tokens :: OAuth
tokens = twitterOAuth
    { oauthConsumerKey = (pack C.oauthConsumerKey)
    , oauthConsumerSecret = (pack C.oauthConsumerSecret)
    }


credential :: Credential
credential = Credential
    [ ((pack "oauth_token"), (pack C.oauthToken))
    , ((pack "oauth_token_secret"), (pack C.oauthTokenSecret))
    ]

twInfo = setCredential tokens credential def


someFunc :: IO ()
someFunc = do
    mgr <- newManager tlsManagerSettings
    timeline <- call twInfo mgr homeTimeline
    print timeline
    return ()
