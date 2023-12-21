import React, { useState } from "react";
import styled from "styled-components";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBars, faTimes } from "@fortawesome/free-solid-svg-icons";
import hongmapLogo from '../../static/logo/hongmapLogo.png'
import MenubarArea from "./menubar";

function Header() {
    const [isToggled, setIsToggled] = useState<boolean>(false);
    return(
      <HeaderContainer>
          <MenuArea onClick={() => {
              setIsToggled(!isToggled);
          }} >
              <FontAwesomeIcon icon={!isToggled ? faBars : faTimes} cursor="pointer"/>
          </MenuArea>
          <LogoArea>
              <img src={hongmapLogo} alt={hongmapLogo} width={280}></img>
          </LogoArea>
          {isToggled &&
              (<MenubarArea />)}
      </HeaderContainer>
    );
}

export default Header;

const HeaderContainer = styled.div`
  height: 127px;
  background-color: white;
  border-bottom: 0.17rem solid #D8D8D8;
  display: flex;
  align-items: center;
`

const LogoArea = styled.div`
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
`

const MenuArea = styled.div`
  position: absolute;
  left: 44px;
  width: 42px;
  height: 70px;
  font-size: xxx-large;
`
