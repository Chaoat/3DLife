#pragma once
#include "EventReceiver.h"

using namespace irr;

MyEventReceiver::MyEventReceiver() {
u32 k;
for (k = 0; k < sizeof(Keys) / sizeof(*Keys); ++k)
      Keys[k] = false;
}

MyEventReceiver::~MyEventReceiver() {
}

// you may need to change the parameter type depending on your Irrlicht version
bool MyEventReceiver::OnEvent(const SEvent& event) {
      if (event.EventType == EET_KEY_INPUT_EVENT)
      {
            Keys[event.KeyInput.Key] = event.KeyInput.PressedDown;
            std::cout << "key: " << event.KeyInput.Key << std::endl;
            return true;
      }

      std::cout << "non-key event" << std::endl;

      return false;
}