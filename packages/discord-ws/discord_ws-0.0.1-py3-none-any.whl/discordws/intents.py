from altflags import Flags, flag

# https://discord.com/developers/docs/topics/gateway#gateway-intents
class Intents(Flags):
    guilds = flag(0)
    guild_members = flag(1)
    guild_bans = flag(2)
    guild_emojis_and_stickers = flag(3)
    guild_integrations = flag(4)
    guild_webhooks = flag(5)
    guild_invites = flag(6)
    guild_voice_states = flag(7)
    guild_presences = flag(8)
    guild_messages = flag(9)
    guild_message_reactions = flag(10)
    guild_message_typing = flag(11)
    direct_messages = flag(12)
    direct_message_typing = flag(13)

    @classmethod
    def all(cls):
        return cls( pow(2, 13) - 1 )