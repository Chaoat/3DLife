#ifndef TRANSFER_DATA_H
#define TRANSFER_DATA_H
#define MAX_CELLS 1048576 /* 1 MiB */
#define MAX_DIMENSIONS 20

struct TransferData
{
    bool drawMode;

    unsigned int dimensions[MAX_DIMENSIONS];

    // on 32bit systems cells will take up 4MB RAM
    // on 64bit systems cells will take up 8MB RAM
    unsigned int cells[MAX_CELLS];
};


#endif // TRANSFER_DATA_H