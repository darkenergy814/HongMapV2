import React, { useState } from "react";
import styled from "styled-components";
import findingWay from "../../static/logo/findingWay.svg";
import club from "../../static/logo/club.svg";
import {SearchingMenu, ClubMenu} from "./menu";

function MenubarArea() {
    const [isFindingWayToggled, setIsFindingWayToggled] = useState<boolean>(false);
    const [isClubToggled, setIsClubToggled] = useState<boolean>(false);
    return (
        <MenubarContainer>
            <Menubar>
                <Menu src={findingWay}
                      onClick={()=>{
                          setIsFindingWayToggled(!isFindingWayToggled)
                          setIsClubToggled(false)}}/>
                <Menu src={club}
                      onClick={()=>{
                          setIsClubToggled(!isClubToggled)
                          setIsFindingWayToggled(false)}}/>
            </Menubar>
            {(isFindingWayToggled) &&
                (<MenuDetailArea>
                    <SearchingMenu />
                </MenuDetailArea>)}
            {(isClubToggled) &&
                (<MenuDetailArea>
                    <ClubMenu />
                </MenuDetailArea>)}
        </MenubarContainer>
    )
}

export default MenubarArea;

const MenubarContainer = styled.div`
`

const Menubar = styled.div`
  position: absolute;
  top: 130px;
  width: 136px;
  height: 100%;
  border-right: 0.17rem solid #D8D8D8;
  background-color: white;
  display: flex;
  flex-direction: column;
`
const Menu = styled.img`
    cursor: pointer;
`

const MenuDetailArea = styled.div`
  position: absolute;
  left: 136px;
  top: 128px;
  width: 360px;
  height: 100%;
  border-right: 0.17rem solid #D8D8D8;
  background-color: white;
  z-index: -1;
`