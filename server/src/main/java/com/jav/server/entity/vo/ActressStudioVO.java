package com.jav.server.entity.vo;

import java.util.List;

import com.jav.server.entity.base.Actress;
import com.jav.server.entity.base.Studio;

import lombok.Data;

@Data
public class ActressStudioVO {
    Actress actress;
    List<Studio> studios;
}
