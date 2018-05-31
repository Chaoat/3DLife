#pragma once
#include <irrlicht.h>

using namespace irr;

class MyEventReceiver : public IEventReceiver
{
    public:
        MyEventReceiver();

        virtual ~MyEventReceiver();

        // you may need to change the parameter type depending on your Irrlicht version
        virtual bool OnEvent(const SEvent& event);

        bool Keys[KEY_KEY_CODES_COUNT];
};