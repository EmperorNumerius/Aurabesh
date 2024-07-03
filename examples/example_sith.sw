Set Path ~~> Sith:/
    Set x = 5;
    Transmit "Welcome to the Dark Side!";
    ForceChoke "Sith";
    ForceChoke {1, 2, 3};
    Transmit "Enemy health after Force Choke";
    Switch x: 1 => One; 2 => Two;
    ForEach {1, 2, 3}: {
        print(item);
    };
    Try {
        print(1/0);
    }: {
        print("Error!");
    };
    While x < 5: {
        print(x);
        x += 1;
    };
