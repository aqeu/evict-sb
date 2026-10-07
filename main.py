import os, sys, re, discord, asyncio, json
import random, time, threading, requests
from discord.ext import commands, tasks
class EvictSelfbot:
      def __init__(self):
          self.token = self.get_token()
          self.prefix = "!"
          self.client = discord.Client()
          self.autoreact_enabled = False
          self.autoreply_enabled = False
          self.spam_mode = False
          self.nuke_mode = False
          self.rickroll_mode = False
          self.insult_mode = False
          self.spam_words = ["FUCK", "DIE", "LOL", "NIGGER", "FAGGOT", "CUNT", "BITCH"]
          self.insults = [
              "You're a fucking retard",
              "Your mom is a whore",
              "Go kill yourself",
              "You're worthless",
              "Fucking cumdumpster",
              "Eat shit and die",
              "You're a piece of shit",
              "Go fuck yourself"
          ]
          self.rickroll_links = [
              "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
              "https://www.youtube.com/watch?v=oHg5SJYRHA0",
              "https://www.youtube.com/watch?v=DLzxrzFCyOs"
          ]

          self.setup_events()

      def setup_events(self):
          @self.client.event
          async def on_ready():
              print(f"Logged in as {self.client.user}")
              print("SB active!")

          @self.client.event
          async def on_message(message):
              if message.author == self.client.user:
                  return
              if self.autoreact_enabled:
                  await self.autoreact(message)
              if self.autoreply_enabled:
                  await self.autoreply(message)
              if message.content.startswith(self.prefix):
                  await self.process_hostile_commands(message)

          @self.client.event
          async def on_reaction_add(reaction, user):
              if user == self.client.user:
                  return
              if self.autoreact_enabled:
                  await self.react_to_reaction(reaction, user)

      def get_token(self):
          if os.path.exists("token.txt"):
              with open("token.txt", "r") as f:
                  return f.read().strip()
          else:
              token = input("Enter your Discord token: ")
              with open("token.txt", "w") as f:
                  f.write(token)
              return token

      async def autoreact(self, message):
          try:
              await message.add_reaction("🔥")
              if any(word in message.content.lower() for word in ["kill", "die", "death", "suicide"]):
                  await message.add_reaction("💀")
              if len(message.content) > 100 or "?" in message.content:
                  await message.add_reaction("🤡")
              if random.random() < 0.1:
                  await message.add_reaction("🖕")
          except:
              pass

      async def autoreply(self, message):
          try:
              if "hello" in message.content.lower():
                  replies = ["Go away", "Fuck off", "Die", "Shut up"]
                  await message.channel.send(random.choice(replies))
              elif "help" in message.content.lower():
                  await message.channel.send("Get fucked")
              elif "sorry" in message.content.lower():
                  await message.channel.send("Too bad, still hate you")
              elif message.mention_everyone:
                  await message.channel.send("@everyone is full of retards")
              if random.random() < 0.05: 
                  await message.channel.send(f"{message.author.mention} {random.choice(self.insults)}")
          except:
              pass

      async def react_to_reaction(self, reaction, user):
          try:
              await reaction.message.add_reaction("🖕")
              if reaction.emoji == "❤️":
                  await reaction.message.add_reaction("💀")
          except:
              pass

      async def process_hostile_commands(self, message):
          command = message.content[len(self.prefix):].split()
          if not command:
              return

          cmd = command[0].lower()
          if cmd == "spam":
              await self.spam_messages(message, command[1:])
          elif cmd == "massspam":
              await self.mass_spam(message)
          elif cmd == "nuke":
              await self.nuke_channel(message)
          elif cmd == "rickroll":
              await self.rickroll_user(message, command[1:])
          elif cmd == "massrickroll":
              await self.mass_rickroll(message)
          elif cmd == "insult":
              await self.insult_user(message, command[1:])
          elif cmd == "massinsult":
              await self.mass_insult(message)
          elif cmd == "react":
              await self.mass_react(message, command[1:])
          elif cmd == "clearr":
              await self.clear_reactions(message, command[1:])
          elif cmd == "hostileon":
              await self.enable_hostile_mode(message)
          elif cmd == "hostileoff":
              await self.disable_hostile_mode(message)
          elif cmd == "destroy":
              await self.destroy_server(message)
          elif cmd == "leaveall":
              await self.leave_all_servers()
          elif cmd == "deleteall":
              await self.delete_all_messages(message)

      async def spam_messages(self, message, args):
          if len(args) < 2:
              await message.channel.send("Usage: !spam <count> <message>")
              return
          try:
              count = int(args[0])
              spam_msg = " ".join(args[1:])
              for i in range(min(count, 50)): 
                  await message.channel.send(spam_msg)
                  await asyncio.sleep(0.5)
          except ValueError:
              await message.channel.send("Invalid number!")

      async def mass_spam(self, message):
          for channel in message.guild.text_channels:
              try:
                  for i in range(5):
                      await channel.send(f"**SPAM BY {message.author}**\nFUCK THIS SERVER")
                      await asyncio.sleep(1)
              except:
                  pass

      async def nuke_channel(self, message):
          await message.channel.send("NUKING CHANNEL...")
          try:
              async for msg in message.channel.history(limit=100):
                  try:
                      await msg.delete()
                      await asyncio.sleep(0.1)
                  except:
                      pass
              for i in range(20):
                  await message.channel.send("@everyone THIS CHANNEL IS SUCK")
                  await asyncio.sleep(0.5)
          except:
              await message.channel.send("Failed to nuke channel twan")

      async def rickroll_user(self, message, args):
          if len(args) < 1:
              await message.channel.send("Usage: !rickroll <@user>")
              return
          user = message.mentions[0] if message.mentions else None
          if user:
              for i in range(10):
                  try:
                      await user.send(random.choice(self.rickroll_links))
                      await asyncio.sleep(1)
                  except:
                      pass
              await message.channel.send(f"Rickrolled {user.mention}")

      async def mass_rickroll(self, message):
          for member in message.guild.members:
              if not member.bot:
                  for i in range(5):
                      try:
                          await member.send(random.choice(self.rickroll_links))
                          await asyncio.sleep(1)
                      except:
                          pass

      async def insult_user(self, message, args):
          if len(args) < 1:
              await message.channel.send("Usage: !insult <@user>")
              return
          user = message.mentions[0] if message.mentions else None
          if user:
              insults = [
                  f"{user.mention} is a fucking cumdumpster",
                  f"{user.mention} should kill themselves",
                  f"{user.mention} is a worthless piece of shit",
                  f"{user.mention} smells like ass",
                  f"{user.mention} is a fucking retard"
              ]
              for insult in insults:
                  await message.channel.send(insult)
                  await asyncio.sleep(1)

      async def mass_insult(self, message):
          for member in message.guild.members:
              if not member.bot:
                  insult = f"{member.mention} {random.choice(self.insults)}"
                  try:
                      await message.channel.send(insult)
                      await asyncio.sleep(0.1)
                  except:
                      pass

      async def mass_react(self, message, args):
          if len(args) < 1:
              await message.channel.send("Usage: !react <emoji>")
              return
          emoji = args[0]
          async for msg in message.channel.history(limit=50):
              try:
                  await msg.add_reaction(emoji)
                  await asyncio.sleep(0.5)
              except:
                  pass

      async def clear_reactions(self, message, args):
          if len(args) < 1:
              async for msg in message.channel.history(limit=1):
                  try:
                      await msg.clear_reactions()
                      await message.channel.send("Cleared reactions")
                  except:
                      await message.channel.send("Failed to clear reactions")
          else:
              try:
                  msg_id = int(args[0])
                  msg = await message.channel.fetch_message(msg_id)
                  await msg.clear_reactions()
                  await message.channel.send("Cleared reactions")
              except:
                  await message.channel.send("Invalid message ID")

      async def enable_hostile_mode(self, message):
          self.autoreact_enabled = True
          self.autoreply_enabled = True
          self.spam_mode = True
          self.rickroll_mode = True
          self.insult_mode = True
          await message.channel.send("**HOSTILE ACTIVATED TWAN**")
          asyncio.create_task(self.hostile_background_task(message.channel))

      async def disable_hostile_mode(self, message):
          self.autoreact_enabled = False
          self.autoreply_enabled = False
          self.spam_mode = False
          self.rickroll_mode = False
          self.insult_mode = False
          await message.channel.send("Hostile disabled nigga")

      async def hostile_background_task(self, channel):
          while self.autoreact_enabled:
              try:
                  members = channel.guild.members
                  random_member = random.choice([m for m in members if not m.bot])
                  await channel.send(f"{random_member.mention} {random.choice(self.insults)}")
                  await channel.send(random.choice(self.spam_words) * 5)
                  await asyncio.sleep(30)
              except:
                  break

      async def destroy_server(self, message):
          await message.channel.send("**DESTROYING THIS FUCKASS SERVER**")
          for channel in message.guild.channels:
              try:
                  await channel.delete()
              except:
                  pass
          for member in message.guild.members:
              if not member.bot and member != message.guild.owner:
                  try:
                      await member.ban(reason="FUCK OFF")
                  except:
                      pass
          try:
              await message.guild.edit(name="DESTROYED SERVER", icon=None)
          except:
              pass

      async def leave_all_servers(self):
          for guild in self.client.guilds:
              try:
                  await guild.leave()
                  print(f"Left server: {guild.name}")
                  await asyncio.sleep(1)
              except:
                  pass

      async def delete_all_messages(self, message):
          deleted = 0
          async for msg in message.channel.history(limit=1000):
              if msg.author == self.client.user:
                  try:
                      await msg.delete()
                      deleted += 1
                      await asyncio.sleep(0.5)
                  except:
                      pass
          await message.channel.send(f"Deleted {deleted} messages")

if __name__ == "__main__":
      print("Starting Selfbot...")
      selfbot = EvictSelfbot()
      selfbot.client.run(selfbot.token, bot=False)
