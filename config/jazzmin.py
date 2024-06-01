from os.path import join
from os import getenv
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(join(Path(__file__).resolve().parent.parent, 'stack.env'))

ADMIN_BRAND_NAME = "Default" if getenv('ADMIN_BRAND_NAME') == '' else getenv('ADMIN_BRAND_NAME')

JAZZMIN_SETTINGS_ORIGINAL = {

    "site_title": f"Admin {ADMIN_BRAND_NAME}",
    "site_header": f"{ADMIN_BRAND_NAME}",
    "site_brand": f"{ADMIN_BRAND_NAME}",
    "site_logo_classes": "img-circle",
    "welcome_sign": f"Welcome to {ADMIN_BRAND_NAME}",
    "topmenu_links": [
        {"name": "Return to Site", "url": "/", "new_window": False},
        {"name": "Admin", "url": "/admin/", "new_window": False},
        {"name": "Control Panel", "permissions": ["raptormc.panel"], "url": "/panel/", "new_window": False},
        {"name": "Discord Bot", "permissions": ["raptormc.discord_bot"], "url": "/panel/discordbot/", "new_window": False},
        {"name": "Server Actions", "permissions": ["raptormc.server_actions"], "url": "/panel/serveractions/", "new_window": False},
        {"name": "Reporting", "permissions": ["raptormc.reporting"], "url": "/panel/reporting/", "new_window": False},
        {"name": "Donations", "permissions": ["raptormc.donations"], "url": "/panel/donations/", "new_window": False},
        {"app": "raptormc"},
        {"app": "gameservers"},
        {"app": "raptorbot"},
        {"app": "donations"},
        {"app": "staffapps"},
        {"app": "authprofiles"},
        {"name": "Settings", "permissions": ["raptormc.settings"],  "url": "/panel/settings/", "new_window": False},
    ],
    "usermenu_links": [
        {"model": "auth.user"},
        {"name": "Return to Site", "url": "/", "new_window": False},
        {"name": "Admin", "url": "/admin/", "new_window": False},
        {"name": "Control Panel", "permissions": ["raptormc.panel"], "url": "/panel/", "new_window": False},
        {"name": "Discord Bot", "permissions": ["raptormc.discord_bot"], "url": "/panel/discordbot/", "new_window": False},
        {"name": "Server Actions", "permissions": ["raptormc.server_actions"], "url": "/panel/serveractions/", "new_window": False},
        {"name": "Reporting", "permissions": ["raptormc.reporting"], "url": "/panel/reporting/", "new_window": False},
        {"name": "Donations", "permissions": ["raptormc.donations"], "url": "/panel/donations/", "new_window": False},
        {"name": "Settings", "permissions": ["raptormc.settings"],  "url": "/panel/settings/", "new_window": False},
    ],

    # Sidebar
    "show_sidebar": True,
    "navigation_expanded": False,
    "hide_apps": ['ipn'],
    "order_with_respect_to": ["raptormc", "gameservers", "raptorbot", 'donations', "staffapps", "authprofiles"],
    "custom_links": {
        "raptorbot": [{
            "name": "Discord Bot Control Panel", 
            "url": "/panel/discordbot/", 
            "icon": "fas fa-terminal",
            "permissions": ["raptormc.discord_bot"]
        }],
         "gameservers": [{
            "name": "Server Actions", 
            "url": "/panel/serveractions/", 
            "icon": "fas fa-terminal",
            "permissions": ["raptormc.server_actions"]
        }],
         "donations": [{
            "name": "Completed Donations", 
            "url": "/panel/donations/", 
            "icon": "fa fa-check-double",
            "permissions": ["raptormc.donations"]
        }],
         "donations": [{
            "name": "Completed Donations", 
            "url": "/panel/donations/", 
            "icon": "fa fa-check-double",
            "permissions": ["raptormc.donations"]
        }]
    },
    "icons": {
        "raptormc": "fas fa-book",
        "raptormc.InformativeText": "fas fa-scroll",
        "raptormc.NavbarLink": "fas fa-map-marker",
        "raptormc.NavbarDropdown": "fas fa-map-marker",
        "raptormc.NavWidget": "fas fa-map-pin",
        "raptormc.NavWidgetBar": "fas fa-map-pin",
        "raptormc.NotificationToast": "fas fa-envelope-square",
        "raptormc.Page": "fas fa-file",
        "gameservers": "fas fa-gamepad",
        "gameservers.Player": "fas fa-headset",
        "gameservers.Server": "fas fa-server",
        "raptorbot": "fas fa-robot",
        "raptorbot.SentEmbedMessage": "fas fa-comment",
        "raptorbot.GlobalAnnouncement": "fas fa-bullhorn",
        "raptorbot.ServerAnnouncement": "fas fa-bullhorn",
        "staffapps": "fas fa-book-reader",
        "staffapps.ModeratorApplication": "fas fa-book-open",
        "staffapps.AdminApplication": "fas fa-book-open",
        "authprofiles": "fas fa-users",
        "authprofiles.RaptorUserGroup": "fas fa-users",
        "authprofiles.RaptorUser": "fas fa-user",
        "authprofiles.UserProfileInfo": "fas fa-user-tag",
        "authprofiles.DiscordUserInfo": "fas fa-user-tag",
        "donations": "fa fa-coins",
        "donations.DonationPackage": "fa fa-archive",
        "donations.DonationServerCommand": "fa fa-terminal",
        "donations.DonationDiscordRole": "fa fa-mask",
        
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,

}

JAZZMIN_UI_TWEAKS_ORIGINAL = {

    "navbar_small_text": True,
    "footer_small_text": True,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-lightblue",
    "navbar": "navbar-gray-dark navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_disable_expand": True,
    "theme": "cyborg",
    "actions_sticky_top": False,
    "sidebar_nav_child_indent": True,

}